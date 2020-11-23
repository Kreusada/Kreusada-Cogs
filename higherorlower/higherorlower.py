import discord
import random
import asyncio

from discord.utils import get

from redbot.core import commands, checks, bank, Config
from redbot.core.utils.predicates import MessagePredicate

class HigherOrLower(commands.Cog):
  """Play higher or lower, win extra cash."""
  
  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(
      self, identifier=5865146514315491, force_registration=True
    )
    
  @commands.command()
  async def higherorlower(self, ctx):
    """Play higher or lower, get awarded currency."""
    currency = await bank.get_currency_name(ctx.guild)
    pred = MessagePredicate.yes_or_no(ctx)
    await ctx.send("Do you want the winner to have a specific role? (yes/no)")
    try:
