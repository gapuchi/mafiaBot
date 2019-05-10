from discord.ext import commands
import discord
import random

orangeTeam = []
blueTeam = []
gameMessage = None

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_reaction_add(reaction, user):
    if gameMessage is not None and reaction.message.id != gameMessage.id:
        return
    

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def new(ctx, numOfMafias: int, *players: discord.Member):
    
    mafia = set(random.choices(players, k=numOfMafias))
    notMafia = set(players) - mafia

    orangeTeam = set(random.choices(players, k=int(len(players)/2)))
    blueTeam = set(players) - orangeTeam

    for player in mafia:
        await player.send("You're Mafia!")
    
    for player in notMafia:
        await player.send("You're Villager!")

    orangeMentions = ",".join(map(lambda x: x.mention, orangeTeam))
    blueMentions = ",".join(map(lambda x: x.mention, blueTeam))

    embed = discord.Embed()
    embed.add_field(name="Blue Team:", value=blueMentions)
    embed.add_field(name="Orange Team:", value=orangeMentions)

    message = await ctx.send("New Game!", embed=embed)
    await message.add_reaction('🔷')
    await message.add_reaction('🔶')
    await message.add_reaction('🏁')

    gameMessage = message

@bot.command()
async def orange(ctx):
    await ctx.send(",".join(map(lambda x: x.mention, orangeTeam)))

bot.run(open("botToken", "r").read())