from redbot.core import commands, checks, Config
import discord
import random
import json
import os
from .mdtembed import Embed
from .featureds import FEATUREDS
from discord.utils import get

class Mcoc(commands.Cog):
  """Mcoc"""
    
  @commands.group(invoke_without_command=True)
  async def crystal(self, ctx):
    """Chooses a random champion from MCOC."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='You got... :gem:')
    image = (random.choice(FEATUREDS))
    name = ctx.author.name
    data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
  @commands.group()
  async def champ(self, ctx):
    """Find champion images."""
    
  @champ.group()
  async def featured(self, ctx):
    """Find champion featured images."""
    data = Embed.create(self, ctx, title='{0} Featured Image')
    image = (random.choice(FEATUREDS))
    name = ctx.author.name
    data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
      
