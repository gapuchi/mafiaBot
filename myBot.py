#! /usr/bin/env python

from discord.ext import commands
import discord
import random
import json

votingChoices = ['1\u20E3','2\u20E3','3\u20E3','4\u20E3','5\u20E3','6\u20E3','7\u20E3','8\u20E3']

teamPlayers = []
orangeTeam = []
blueTeam = []
winningTeam = None
losingTeam = None
mafia = []
villagers = []
gameMessage = None
votingMessage = None
numberedPlayers = None
gameMaster = None

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_reaction_add(reaction, user):
    global votingMessage
    global numberedPlayers
    global winningTeam
    global losingTeam
    global gameMessage

    if user.bot:
        return

    if gameMessage is not None and reaction.message.id == gameMessage.id:
        if user != gameMaster:
            await reaction.remove(user)
            return

        if reaction.emoji == '\U0001F3C1':
            if noWinners(reaction.message):
                await reaction.remove(user)
                return

            votingOptions = votingChoices[:len(teamPlayers)]
            numberedPlayers = dict(zip(votingOptions, teamPlayers))
            numberedPlayersString = "".join("{}-{}".format(vote, player.mention) for [vote, player] in numberedPlayers.items())

            embed = discord.Embed()
            embed.add_field(name="**Players:**", value=numberedPlayersString)

            # Clearing to prevent further modification
            gameMessage = None

            votingMessage = await reaction.message.channel.send("**Vote For Mafia!**", embed = embed)
            for option in votingOptions:
                await votingMessage.add_reaction(option)

        if reaction.emoji == '\U0001F537':
            if tooManyWinners(reaction.message):
                await reaction.remove(user)
                return
            winningTeam = blueTeam
            losingTeam = orangeTeam

        if reaction.emoji == '\U0001F536':
            if tooManyWinners(reaction.message):
                await reaction.remove(user)
                return
            winningTeam = orangeTeam
            losingTeam = blueTeam

    if votingMessage is not None and reaction.message.id == votingMessage.id:
        votes = len([reaction for reaction in reaction.message.reactions if user in await reaction.users().flatten()])
        if votes > len(mafia):
            await reaction.remove(user)
            return

        if reaction.count == 1:
            await reaction.remove(user)
            return

        totalReactions = sum([x.count for x in reaction.message.reactions])
        if totalReactions == (2 * len(teamPlayers)):
            votes = {numberedPlayers[reaction.emoji]:  list(filter(lambda x: not x.bot, await reaction.users().flatten())) for reaction in reaction.message.reactions}
            points = calculatePoints(votes)
            embed = discord.Embed()
            for [user, points] in points.items():
                embed.add_field(name="**{}**".format(user.name), value=points)
            await reaction.message.channel.send("**Points:**", embed=embed)

            # Clearing to prevent further modification
            votingMessage = None

def noWinners(message):
    reactionCount = {reaction.emoji: reaction.count for reaction in message.reactions}
    return reactionCount['\U0001F537'] == 1 and reactionCount['\U0001F536'] == 1

def tooManyWinners(message):
    reactionCount = {reaction.emoji: reaction.count for reaction in message.reactions}
    return reactionCount['\U0001F537'] > 1 and reactionCount['\U0001F536'] > 1

def calculatePoints(votes):
    points = dict((player, 0) for player in teamPlayers)
    with open("config/points.json") as json_file:
        pointValues = json.load(json_file)
        villagerPointValues = pointValues['villager']
        mafiaPointValues =  pointValues['mafia']

    for m in mafia:
        # Guessed mafia
        for player in votes[m]:
            if player not in mafia:
                points[player] += villagerPointValues['guessedMafia']

        # Mafia not chosen in majority
        if len(votes[m]) * 2 < len(teamPlayers):
            points[m] += mafiaPointValues['notKilled']
        # Killed mafia
        else:
            for villager in villagers:
                points[villager] += villagerPointValues['killedMafia']

        # No votes against mafia
        if len(votes[m]) == 0:
            points[m] += mafiaPointValues['noVotesAgainst']

    # Mafia losing game
    for player in losingTeam:
        if player in mafia:
            points[player] += mafiaPointValues['teamLost']

    # Winning game
    for player in winningTeam:
        if player not in mafia:
            points[player] += villagerPointValues['teamWon']

        if player in mafia:
            points[player] += mafiaPointValues['teamWon']
            points[player] *= mafiaPointValues['teamWonMultiplier']

    return points

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def new(ctx, numOfMafias: int, *players: discord.Member):
    global teamPlayers
    global orangeTeam
    global blueTeam
    global mafia
    global villagers
    global gameMessage
    global gameMaster

    if gameMessage is not None:
        await ctx.send("**Game in progress!**")
        return

    gameMaster = ctx.author

    # Setting teams
    teamPlayers = list(players)
    random.shuffle(teamPlayers)
    splittingIndex = int(len(teamPlayers) / 2 + random.uniform(0.25,0.75))
    orangeTeam = teamPlayers[splittingIndex:]
    blueTeam = teamPlayers[:splittingIndex]

    # Setting mafia
    teams = [orangeTeam, blueTeam]
    random.shuffle(teams)

    numMafiasTeam1 = int(numOfMafias / 2 + random.uniform(0.25,0.75))
    numMafiasTeam2 = numOfMafias - numMafiasTeam1

    mafia = []
    mafia.extend(set(random.choices(teams[0], k = numMafiasTeam1)))
    mafia.extend(set(random.choices(teams[1], k = numMafiasTeam2)))

    villagers = set(teamPlayers) - set(mafia)

    # Notifying players of roles
    for player in teamPlayers:
        await player.send("You're {} on the {} team!".format("Mafia" if player in mafia else "Villager", "Orange" if player in orangeTeam else "Blue"))

    # Notify players of teams

    orangeMentions = ",".join(x.mention for x in orangeTeam)
    blueMentions = ",".join(x.mention for x in blueTeam)

    embed = discord.Embed()
    embed.add_field(name="**Blue Team:**", value=blueMentions)
    embed.add_field(name="**Orange Team:**", value=orangeMentions)
    embed.add_field(name="**Game Result:**", value="**Blue Won:\U0001F537 Orange Won:\U0001F536 Finish:\U0001F3C1**")

    message = await ctx.send("**New Game!**", embed=embed)
    await message.add_reaction('\U0001F537')
    await message.add_reaction('\U0001F536')
    await message.add_reaction('\U0001F3C1')

    gameMessage = message

@bot.command()
async def end(ctx):
    global gameMessage
    gameMessage = None

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

with open("secrets/botToken", "r") as tokenf:
    bot.run(tokenf.read().rstrip())
