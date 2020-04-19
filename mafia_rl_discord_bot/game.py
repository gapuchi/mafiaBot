import discord
from discord.ext import commands

from .voting import Voting


class Game(commands.Cog):

    votingChoices = ['1\u20E3', '2\u20E3', '3\u20E3', '4\u20E3', '5\u20E3', '6\u20E3', '7\u20E3', '8\u20E3']

    def __init__(self, bot, message, game_master, players, blue_team, orange_team, mafia, villagers):
        self.bot = bot
        self.message = message
        self.gameMaster = game_master
        self.players = players
        self.blueTeam = blue_team
        self.orangeTeam = orange_team
        self.mafia = mafia
        self.villagers = villagers

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        if user.bot:
            return

        if reaction.message.id != self.message.id:
            return

        if user != self.gameMaster:
            await reaction.remove(user)
            return

        if reaction.emoji == '\U0001F537':
            if self.too_many_winners(reaction.message):
                await reaction.remove(user)
                return
            await self.set_voting(reaction, self.blueTeam, self.orangeTeam)
        elif reaction.emoji == '\U0001F536':
            if self.too_many_winners(reaction.message):
                await reaction.remove(user)
                return
            await self.set_voting(reaction, self.orangeTeam, self.blueTeam)
        else:
            await reaction.remove(user)
            return

    async def set_voting(self, reaction, winning_team, losing_team):
        voting_options = Game.votingChoices[:len(self.players)]
        numbered_players = dict(zip(voting_options, self.players))
        numbered_players_string = "".join(
            "{}-{}".format(vote, player.mention) for (vote, player) in numbered_players.items())

        embed = discord.Embed()
        embed.add_field(name="**Players:**", value=numbered_players_string)

        voting_message = await reaction.message.channel.send("**Vote For Mafia!**", embed=embed)

        for option in voting_options:
            await voting_message.add_reaction(option)

        self.bot.remove_cog('Game')

        self.bot.add_cog(
            Voting(self.bot, self.mafia, self.players, numbered_players, voting_message, losing_team, winning_team,
                   self.villagers))

    @staticmethod
    def no_winners(message):
        reaction_count = {reaction.emoji: reaction.count for reaction in message.reactions}
        return reaction_count['\U0001F537'] == 1 and reaction_count['\U0001F536'] == 1

    @staticmethod
    def too_many_winners(message):
        reaction_count = {reaction.emoji: reaction.count for reaction in message.reactions}
        return reaction_count['\U0001F537'] > 1 and reaction_count['\U0001F536'] > 1
