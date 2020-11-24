import discord
import random
import asyncio
from random import randint
from .rtbresources import Embed
from discord.utils import get
from redbot.core import commands, checks, bank, Config
from redbot.core.utils.predicates import MessagePredicate

class RobTheBank(commands.Cog):
  """Rob the bank, gain or get fined!"""

  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(
      self, identifier=5865146514315491, force_registration=True
    )
   
  @commands.command()
  @commands.cooldown(1, 300, BucketType)
  async def rob(self, ctx):
    """Attempt to rob the bank. Attempt."""
    resu = random.randint(RESU)
    status = f"{ctx.author.name} attempted to rob the bank..."
    if resu > 4:
      title = status
      description = random.choice(UNSUCRESP)
    else:
      title = status
      description = random.choice(SUCRESP)
    data = Embed.create(self, ctx, title=title, description=description)
      
      
