from redbot.core import commands, checks, Config
import discord
import random
import json
import os
from .mdtembed import Embed
from .featureds import FEATUREDS
from .featureds import FULL_NAMES
from .featureds import ALIASES
from .portraits import PORTRAITS
from .crystal import CRYSTAL
from discord.utils import get


class Mcoc(commands.Cog):
    """Fun Games and Tools for Marvel Contest of Champions."""
    
    @commands.group(invoke_without_command=True)
    async def mdtlink(self, ctx):
        """Matrix Development Team invite link."""
        await ctx.send("https://discord.gg/JmCFyq7")

    @commands.group(invoke_without_command=True)
    async def crystal(self, ctx):
        """Chooses a random champion from MCOC."""
        await ctx.send("`I'm getting this command rebuild right now!` :star_struck:\nFor more updates, please stay tuned to my support server: https://discord.gg/JmCFyq7")
        # author = ctx.message.author
#        data = Embed.create(self, ctx, title='You got... :gem:')
#        image = (random.choice(CRYSTAL))
#        data.set_image(url=image)
#        await ctx.send(embed=data)

    @commands.group()
    async def champ(self, ctx):
        """Find champion images."""

    @champ.command()
    async def featured(self, ctx, alias: str):
        await ctx.send("`I'm getting this command rebuild right now!` :star_struck:\nFor more updates, please stay tuned to my support server: https://discord.gg/JmCFyq7")
#        champion = FULL_NAMES.get(alias, alias)
#        try:
#            data = Embed.create(self, ctx, title="Featured Image.".format(
#                champion.capitalize()), image=FEATUREDS[champion.lower()])
#            await ctx.send(embed=data)
#        except KeyError:
#            await ctx.send("`I could not find that champion.`\n`Please check your spelling, or your alias might not be available just yet.` :fearful:\n\n`Additionally, this command has not yet been completed. I'm working on it asap!`")

    @champ.command()
    async def portrait(self, ctx, champion: str):
        champion = FULL_NAMES.get(alias, alias)
        try:
            data = Embed.create(self, ctx, title="{0}'s Portrait Image.".format(
                champion.capitalize()), image=PORTRAITS[champion.lower()])
            await ctx.send(embed=data)
        except KeyError:
            await ctx.send("`I could not find that champion.`\n`Please check your spelling, or your alias might not be available just yet.` :fearful:\n\n`Additionally, this command has not yet been completed. I'm working on it asap!`")
