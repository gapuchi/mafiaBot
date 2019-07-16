#! /usr/bin/env python

from discord.ext import commands
import discord
import random
import json

from Voting import Voting

votingChoices = ['1\u20E3', '2\u20E3', '3\u20E3', '4\u20E3', '5\u20E3', '6\u20E3', '7\u20E3', '8\u20E3']

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
pointsShown = False

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_reaction_add(reaction, user):
    global votingMessage
    global numberedPlayers
    global winningTeam
    global losingTeam
    global gameMessage
    global pointsShown

    if user.bot:
        return

    if gameMessage is not None and reaction.message.id == gameMessage.id:
        if user != gameMaster:
            await reaction.remove(user)
            return

        if reaction.emoji == '\U0001F3C1':
            if no_winners(reaction.message):
                await reaction.remove(user)
                return

            voting_options = votingChoices[:len(teamPlayers)]
            numberedPlayers = dict(zip(voting_options, teamPlayers))
            numbered_players_string = "".join(
                "{}-{}".format(vote, player.mention) for [vote, player] in numberedPlayers.items())

            embed = discord.Embed()
            embed.add_field(name="**Players:**", value=numbered_players_string)

            # Clearing to prevent further modification
            gameMessage = None

            votingMessage = await reaction.message.channel.send("**Vote For Mafia!**", embed=embed)

            for option in voting_options:
                await votingMessage.add_reaction(option)

            bot.add_cog(Voting(bot, mafia, teamPlayers, numberedPlayers, votingMessage, numberedPlayers, losingTeam,
                               winningTeam, villagers))

        if reaction.emoji == '\U0001F537':
            if too_many_winners(reaction.message):
                await reaction.remove(user)
                return
            winningTeam = blueTeam
            losingTeam = orangeTeam

        if reaction.emoji == '\U0001F536':
            if too_many_winners(reaction.message):
                await reaction.remove(user)
                return
            winningTeam = orangeTeam
            losingTeam = blueTeam


def no_winners(message):
    reaction_count = {reaction.emoji: reaction.count for reaction in message.reactions}
    return reaction_count['\U0001F537'] == 1 and reaction_count['\U0001F536'] == 1


def too_many_winners(message):
    reaction_count = {reaction.emoji: reaction.count for reaction in message.reactions}
    return reaction_count['\U0001F537'] > 1 and reaction_count['\U0001F536'] > 1


def calculate_points(votes):
    points = dict((player, 0) for player in teamPlayers)
    with open("config/points.json") as json_file:
        point_values = json.load(json_file)
        villager_point_values = point_values['villager']
        mafia_point_values = point_values['mafia']

    for m in mafia:
        # Guessed mafia
        for player in votes[m]:
            if player not in mafia:
                points[player] += villager_point_values['guessedMafia']

        # Mafia not chosen in majority
        if len(votes[m]) * 2 < len(teamPlayers):
            points[m] += mafia_point_values['notKilled']
        # Killed mafia
        else:
            for villager in villagers:
                points[villager] += villager_point_values['killedMafia']

        # No votes against mafia
        if len(votes[m]) == 0:
            points[m] += mafia_point_values['noVotesAgainst']

    # Mafia losing game
    for player in losingTeam:
        if player in mafia:
            points[player] += mafia_point_values['teamLost']

    # Winning game
    for player in winningTeam:
        if player not in mafia:
            points[player] += villager_point_values['teamWon']

        if player in mafia:
            points[player] += mafia_point_values['teamWon']
            points[player] *= mafia_point_values['teamWonMultiplier']

    return points


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def new(ctx, num_of_mafias: int):
    await initialize_game(ctx, num_of_mafias, ctx.author.voice.channel.members)


@bot.command()
async def f(ctx, num_of_mafias: int, *players: discord.Member):
    await initialize_game(ctx, num_of_mafias, list(players))


async def initialize_game(ctx, num_of_mafias: int, members):
    global teamPlayers
    global orangeTeam
    global blueTeam
    global mafia
    global villagers
    global gameMessage
    global gameMaster
    global pointsShown

    pointsShown = False

    if gameMessage is not None:
        await ctx.send("**Game in progress!**")
        return

    gameMaster = ctx.author

    # Setting teams
    teamPlayers = members
    random.shuffle(teamPlayers)
    splitting_index = int(len(teamPlayers) / 2 + random.uniform(0.25, 0.75))
    orangeTeam = teamPlayers[splitting_index:]
    blueTeam = teamPlayers[:splitting_index]

    # Setting mafia
    teams = [orangeTeam, blueTeam]
    random.shuffle(teams)

    num_mafias_team1 = int(num_of_mafias / 2 + random.uniform(0.25, 0.75))
    num_mafias_team2 = num_of_mafias - num_mafias_team1

    mafia = []
    mafia.extend(set(random.choices(teams[0], k=num_mafias_team1)))
    mafia.extend(set(random.choices(teams[1], k=num_mafias_team2)))

    villagers = set(teamPlayers) - set(mafia)

    # Notifying players of roles
    for player in teamPlayers:
        await player.send("You're {} on the {} team!".format("Mafia" if player in mafia else "Villager",
                                                             "Orange" if player in orangeTeam else "Blue"))

    # Notify players of teams

    orange_mentions = ",".join(x.mention for x in orangeTeam)
    orange_mentions = orange_mentions if orange_mentions else "No one"
    blue_mentions = ",".join(x.mention for x in blueTeam)
    blue_mentions = blue_mentions if blue_mentions else "No one"
    embed = discord.Embed()
    embed.add_field(name="**Blue Team:**", value=blue_mentions)
    embed.add_field(name="**Orange Team:**", value=orange_mentions)
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


with open("secrets/botToken", "r") as token:
    bot.run(token.read().rstrip())
