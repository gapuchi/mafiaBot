import json

import discord
from discord.ext import commands


class Voting(commands.Cog):

    def __init__(self, bot, mafia, players, voting_options, message, losing_team, winning_team,
                 villagers):
        self.bot = bot
        self.mafia = mafia
        self.players = players
        # Map from emoji to mention
        self.voting_options = voting_options
        self.message = message
        self.losing_team = losing_team
        self.winning_team = winning_team
        self.villagers = villagers

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        if user.bot:
            return

        if reaction.message.id != self.message.id:
            return

        votes = len([reaction for reaction in reaction.message.reactions if user in await reaction.users().flatten()])
        if votes > len(self.mafia):
            await reaction.remove(user)
            return

        if reaction.emoji not in self.voting_options:
            await reaction.remove(user)
            return

        total_reactions = sum([x.count for x in reaction.message.reactions])
        if total_reactions < (len(self.mafia) + 1) * len(self.players):
            return

        votes = {
            self.voting_options[reaction.emoji]: list(filter(lambda x: not x.bot, await reaction.users().flatten()))
            for reaction in reaction.message.reactions}
        points = self.calculate_points(votes)
        embed = discord.Embed()
        for [user, points] in points.items():
            embed.add_field(name="**{}**".format(user.name), value=points)
        await reaction.message.channel.send("**Points:**", embed=embed)
        self.bot.remove_cog('Voting')

    def calculate_points(self, votes):
        points = dict((player, 0) for player in self.players)
        with open("config/points.json") as json_file:
            point_values = json.load(json_file)
            villager_point_values = point_values['villager']
            mafia_point_values = point_values['mafia']

        for m in self.mafia:
            # Guessed mafia
            for player in votes[m]:
                if player not in self.mafia:
                    points[player] += villager_point_values['guessedMafia']

            # Mafia not chosen in majority
            if len(votes[m]) * 2 < len(self.players):
                points[m] += mafia_point_values['notKilled']
            # Killed mafia
            else:
                for villager in self.villagers:
                    points[villager] += villager_point_values['killedMafia']

            # No votes against mafia
            if len(votes[m]) == 0:
                points[m] += mafia_point_values['noVotesAgainst']

        # Mafia losing game
        for player in self.losing_team:
            if player in self.mafia:
                points[player] += mafia_point_values['teamLost']

        # Winning game
        for player in self.winning_team:
            if player not in self.mafia:
                points[player] += villager_point_values['teamWon']

            if player in self.mafia:
                points[player] += mafia_point_values['teamWon']
                points[player] *= mafia_point_values['teamWonMultiplier']

        return points
