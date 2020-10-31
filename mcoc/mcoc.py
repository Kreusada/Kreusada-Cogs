from redbot.core import commands, checks, Config
import discord
import random
import json
import os
from .mdtembed import Embed
from .crystal import CRYSTAL, FEATUREDS, BCB
from discord.utils import get


class Mcoc(commands.Cog):
    """Fun Games and Tools for Marvel Contest of Champions."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=153607829, force_registration=True)
        self.config.register_guild()

    @commands.group(invoke_without_command=True)
    async def vslink(self, ctx):
        """VanguardSkein invite link."""
        await ctx.send("https://discord.gg/JmCFyq7")

    @commands.group(invoke_without_command=True,)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def crystal(self, ctx,):
        """Chooses a random champion from MCOC."""
        data = Embed.create(self, ctx, title='You got... :gem:')
        image = (random.choice(CRYSTAL))
        description = ""
        data.description = description
        data.set_image(url=image)
        await ctx.send(embed=data)

    @commands.group()
    async def battlechip(self, ctx,):
        """Opens a battlechip crystal from MCOC."""

    @battlechip.group(invoke_without_command=True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def basic(self, ctx):
        """Open a basic battlechip crystal."""
        print("[BCB]", random.__file__)
        data = Embed.create(self, ctx)
        drop_rate = random.randint(1, 100)
        if drop_rate < 0.02:
            link = BCB[0]
            title = "4 Star Punisher"
            description = "This tier has a `0.02%` chance.\nCongratulations!\nMessage Kreusada#0518 with a screenshot to be added to the hall of fame!"
        elif drop_rate < 0.65:
            link = BCB[0]
            title = "3 Star Punisher"
            description = "This tier has a `0.65%` chance.\nCongratulations!"
        elif drop_rate < 0.35:
            link = BCB[1]
            title = "Energy Refill"
            description = "This tier has a `0.35%` chance.\nCongratulations!"
        elif drop_rate < 2:
            link = BCB[2]
            title = "45 Units"
            description = ""
        elif drop_rate < 6:
            link = BCB[2]
            title = "15 Units"
            description = ""
        elif drop_rate < 30:
            link = BCB[3]
            title = "10,000 Gold"
            description = ""
        else:
            link = BCB[3]
            title = "2,500 Gold"
            description = ""
        data.title = "You got {}!".format(title)
        data.description = "{}".format(description)
        data.set_image(url=link)
        await ctx.send(embed=data)
        
    @battlechip.group(invoke_without_command=True)
    async def uncollected(self, ctx):
        """Open an uncollected battlechip crystal."""
        data = Embed.create(self, ctx)
        drop_rate = random.randint(1, 100)
        if drop_rate < 0.02:
            link = BCB[0]
            title = "5 Star Punisher"
            description = "This tier has a `0.02%` chance.\nCongratulations!\nMessage Kreusada#0518 with a screenshot to be added to the hall of fame!"
        elif drop_rate < 0.65:
            link = BCB[0]
            title = "4 Star Punisher"
            description = "This tier has a `0.65%` chance.\nCongratulations!"
        elif drop_rate < 0.35:
            link = BCB[1]
            title = "Five Energy Refills"
            description = "This tier has a `0.35%` chance.\nCongratulations!"
        elif drop_rate < 2:
            link = BCB[2]
            title = "225 Units"
            description = ""
        elif drop_rate < 6:
            link = BCB[2]
            title = "75 Units"
            description = ""
        elif drop_rate < 30:
            link = BCB[3]
            title = "50,000 Gold"
            description = ""
        elif drop_rate < 45:
            link = BCB[3]
            title = "25,000 Gold"
            description = ""
        else:
            link = BCB[3]
            title = "10,000 Gold"
            description = ""
        data.title = "You got {}!".format(title)
        data.description = "{}".format(description)
        data.set_image(url=link)
        await ctx.send(embed=data)
