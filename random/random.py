from redbot.core import commands, checks, Config
from .mdtembed import Embed
from discord.utils import get
from .fhm import FHM
import discord
import random

class Random(commands.Cog):
  """Random choice for multiple subjects."""
  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(
      self, identifier=153607829, force_registration=True)
    
  @commands.group(invoke_without_command=True) 
  @commands.cooldown(1, 10, commands.BucketType.user)
  async def futurehousemusic(self, ctx):
    """Chooses a random song from FHM."""
    data = Embed.create(self, ctx, title='You got... :gem:')
    description = (random.choice(FHM))
    data.set_description(url=description)
    await ctx.send(embed=data)
