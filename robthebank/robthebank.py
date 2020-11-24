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
  defaults = {
    "Fine": 400,
    "Deposti": 400,
  }

  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(
      self, identifier=5865146514315491, force_registration=True
    )
    self.config.register_guild(**self.defaults)

  async def red_delete_data_for_user(self, **kwargs):
      """Nothing to delete."""
      return
   
  @commands.command()
  @commands.cooldown(1, 300, commands.BucketType.user)
  async def rob(self, ctx):
    """Attempt to rob the bank. Attempt."""
    resu = random.randint(RESU)
    status = f"{ctx.author.name} attempted to rob the bank..."
    if resu > 4:
      title = status
      description = random.choice(UNSUCRESP)
      await bank.withdraw_credits(ctx.author, settings["Fine"])
    else:
      title = status
      description = random.choice(SUCRESP)
      await bank.deposit_credits(ctx.author, settings["Deposti"])
    data = Embed.create(self, ctx, title=title, description=description)
    await ctx.send(embed=data)
    
  @commands.group()
  async def rtbset(self, ctx):
    """Configurations for robbing the bank."""
    
  @rtbset.command()
  async def deposit(self, ctx, amount: int)
    
      
      
