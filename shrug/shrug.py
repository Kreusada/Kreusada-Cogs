import discord
from redbot.core import commands

class Shrug(commands.Cog):
  """¯\_(ツ)_/¯"""
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  async def shrug(self, ctx, *, message: str):
    """¯\_(ツ)_/¯"""
    await ctx.send(''.join((message, '¯\_(ツ)_/¯')))
