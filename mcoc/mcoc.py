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
        self.config.register_user(roster={})

    @commands.group(invoke_without_command=True)
    async def vslink(self, ctx):
        """VanguardSkein invite link."""
        await ctx.send("https://discord.gg/JmCFyq7")

    @commands.group(invoke_without_command=True,)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def crystal(self, ctx,):
        """Chooses a random champion from MCOC."""
        # author = ctx.message.author
        data = Embed.create(self, ctx, title='You got... :gem:')
        image = (random.choice(CRYSTAL))
        data.set_image(url=image)
        await ctx.send(embed=data)

    @commands.group()
    async def battlechip(self, ctx,):
        """Opens a battlechip crystal from MCOC."""

    @battlechip.group(invoke_without_command=True)
#    @commands.cooldown(1, 10, commands.BucketType.user)
    async def basic(self, ctx):
        """Open a basic battlechip crystal."""
        print("[BCB]", random.__file__)
        data = Embed.create(self, ctx)
        drop_rate = random.randint(1, 100)
        if drop_rate >= 85:
            msg = BCB[0]
            title = "Punisher"
        elif drop_rate >= 70:
            msg = BCB[1]
            title = "Energy refill"
        elif drop_rate >= 45:
            msg = BCB[2]
            title = "Units"
        else:
            msg = BCB[3]
            title = "Gold"
        data.title = "You got {}!".format(title)
        # if drop_rate == 100:
        #     data.title = "You got {}!".format(BCB["4 Star Punisher"])
        # elif drop_rate >= 97:
        #     data.title = "You got {}!".format(BCB["Energy Refill"])
        # elif drop_rate >= 75:
        #     data.title = "You got {}!".format(BCB["3 Star Punisher"])
        # elif drop_rate >= 40:
        #     data.title = "You got {}!".format(BCB["45 Units"])
        # elif drop_rate >= 20:
        #     data.title = "You got {}!".format(BCB["15 Units"])
        # elif drop_rate >= 15:
        #     data.title = "You got {}!".format(BCB[])
        # elif drop_rate >= 10:
        #     data.title = "You got {}!".format(BCB["5,000 Gold"])
        # else:
        #     data.title = "You got {}!".format(BCB["2,000 Gold"])
        data.set_image(url=msg)
        await ctx.send(embed=data)
