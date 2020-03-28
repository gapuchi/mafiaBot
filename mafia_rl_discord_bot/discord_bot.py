#! /usr/bin/env python

from discord.ext import commands
import discord
import random
import logging
from appdirs import AppDirs
import os
from .game import Game

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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
    team_players = members
    random.shuffle(team_players)

    # Setting teams, mafia, and villagers
    orange_team, blue_team = random.sample([team_players[::2], team_players[1::2]], k=2)
    mafias = team_players[:num_of_mafias]
    villagers = team_players[num_of_mafias:]

    # Notifying players of roles
    for player in team_players:
        await player.send("You're {} on the {} team!".format("Mafia" if player in mafias else "Villager",
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

    bot.add_cog(Game(bot, message, ctx.author, team_players, blue_team, orange_team, mafias, villagers))


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


def run_bot():
    app_name = "mafiarldiscordbot"
    app_author = "gapuchi"
    dirs = AppDirs(app_name, app_author)
    config_path = dirs.user_config_dir
    token_path = os.path.join(config_path, 'secrets', 'botToken')
    with open(token_path, "r") as token:
        bot.run(token.read().rstrip())
