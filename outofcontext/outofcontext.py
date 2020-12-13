from .ooc_index import RANDOMWORDS
from redbot.core import commands
import discord
import random

class OutOfContext(commands.Cog):
  """Choose a random word from 50,000."""
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  async def randomword(self, ctx):
    """Choose a random word from 50,000"""
    await ctx.send(f"Random word: {random.choice(RANDOMWORDS)}")
