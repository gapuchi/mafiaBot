from discord.ext import commands
import discord
import random

teamPlayers = []
orangeTeam = []
blueTeam = []
mafia = []
gameMessage = None
votingChoices = ['1\u20E3','2\u20E3','3\u20E3','4\u20E3','5\u20E3','6\u20E3','7\u20E3','8\u20E3']

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if gameMessage is None or reaction.message.id != gameMessage.id:
        return

    if reaction.emoji == '\U0001F3C1':
        votingOptions = votingChoices[:len(teamPlayers)]
        numberedPlayers = list(zip(votingOptions, teamPlayers))
        numberedPlayersString = "".join(map(lambda x: x[0] + "-" + str(x[1].mention), numberedPlayers))

        embed = discord.Embed()
        embed.add_field(name="Players:", value=numberedPlayersString)
       
        message = await reaction.message.channel.send("**Vote For Mafia!**", embed = embed)
        for option in votingOptions:
                await message.add_reaction(option)

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
    global gameMessage

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

    mafia.extend(set(random.choices(teams[0], k = numMafiasTeam1)))
    mafia.extend(set(random.choices(teams[1], k = numMafiasTeam2)))

    # Notifying players of roles
    for player in teamPlayers:
        if player in mafia:
            await player.send("You're Mafia!")
        else:
            await player.send("You're Villager!")

    # Notify players of teams
    orangeMentions = ",".join(map(lambda x: x.mention, orangeTeam))
    blueMentions = ",".join(map(lambda x: x.mention, blueTeam))

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
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(open("botToken", "r").read())