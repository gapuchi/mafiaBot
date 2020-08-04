#! /usr/bin/env python

from discord.ext import commands
import discord
import random
import logging
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
        await ctx.send('Invalid command passed...')


@bot.group()
async def game(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid command passed...')


@game.command(help='Creates teams using the members on the voice channel.')
async def new(ctx):
    if ctx.author.voice is None:
        await ctx.send('You are not on a voice channel.')
    else:
        await initialize_game(ctx, 0, ctx.author.voice.channel.members)


@game.command(name='with', help='Creates teams using only the members provided.')
async def with_players(ctx, *players: discord.Member):
    await initialize_game(ctx, 0, list(players))


@mafia.command(help='Creates teams using the members on the voice channel.')
async def new(ctx, num_of_mafias: int):
    if ctx.author.voice is None:
        await ctx.send('You are not on a voice channel.')
    else:
        await initialize_game(ctx, num_of_mafias, ctx.author.voice.channel.members)


@mafia.command(name='with', help='Creates teams using only the members provided.')
async def with_players(ctx, num_of_mafias: int, *players: discord.Member):
    await initialize_game(ctx, num_of_mafias, list(players))


@bot.command(name='self_destruct')
@commands.is_owner()
async def shutdown(ctx):
    await ctx.bot.logout()


async def initialize_game(ctx, num_of_mafias: int, members):
    team_players = [x for x in members if not x.bot]

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


def get_token() -> str:
    from pathlib import Path
    from appdirs import AppDirs

    dirs = AppDirs("mafiarldiscordbot", "gapuchi")
    token_path = Path(dirs.user_config_dir) / "secrets" / "botToken"

    try:
        with open(token_path) as f:
            return f.read().rstrip()
    except FileNotFoundError:
        pass

    token = input('Enter your bot token: ')
    token_path.parent.mkdir(parents=True, exist_ok=True)
    with open(token_path, "w") as f:
        f.write(token)

    return token


def run_bot() -> None:
    bot.run(get_token())
