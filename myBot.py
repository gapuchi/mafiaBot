#! /usr/bin/env python

from discord.ext import commands
import discord
import random

from Game import Game

bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.group()
async def mafia(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid git command passed...')


@mafia.command()
async def new(ctx, num_of_mafias: int):
    await initialize_game(ctx, num_of_mafias, ctx.author.voice.channel.members)


@mafia.command()
async def f(ctx, num_of_mafias: int, *players: discord.Member):
    await initialize_game(ctx, num_of_mafias, list(players))


async def initialize_game(ctx, num_of_mafias: int, members):

    # Setting teams
    team_players = members
    random.shuffle(team_players)
    splitting_index = int(len(team_players) / 2 + random.uniform(0.25, 0.75))
    orange_team = team_players[splitting_index:]
    blue_team = team_players[:splitting_index]

    # Setting mafia
    teams = [orange_team, blue_team]
    random.shuffle(teams)

    num_mafias_team1 = int(num_of_mafias / 2 + random.uniform(0.25, 0.75))
    num_mafias_team2 = num_of_mafias - num_mafias_team1

    mafia = []
    mafia.extend(set(random.choices(teams[0], k=num_mafias_team1)))
    mafia.extend(set(random.choices(teams[1], k=num_mafias_team2)))

    villagers = set(team_players) - set(mafia)

    # Notifying players of roles
    for player in team_players:
        await player.send("You're {} on the {} team!".format("Mafia" if player in mafia else "Villager",
                                                             "Orange" if player in orange_team else "Blue"))

    # Notify players of teams

    orange_mentions = ",".join(x.mention for x in orange_team)
    orange_mentions = orange_mentions if orange_mentions else "No one"
    blue_mentions = ",".join(x.mention for x in blue_team)
    blue_mentions = blue_mentions if blue_mentions else "No one"

    embed = discord.Embed()
    embed.add_field(name="**Blue Team:**", value=blue_mentions)
    embed.add_field(name="**Orange Team:**", value=orange_mentions)
    embed.add_field(name="**Game Result:**", value="**\U0001F537 - Blue Won\n\U0001F536 - Orange Won**")

    message = await ctx.send("**New Game!**", embed=embed)
    await message.add_reaction('\U0001F537')
    await message.add_reaction('\U0001F536')

    bot.add_cog(Game(bot, message, ctx.author, team_players, blue_team, orange_team, mafia, villagers))


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


with open("secrets/botToken", "r") as token:
    bot.run(token.read().rstrip())
