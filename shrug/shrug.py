import discord
from redbot.core import commands

class Shrug(commands.Cog):
  """¯\_(ツ)_/¯"""
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  async def shrug(self, ctx, *, message: str):
    """¯\_(ツ)_/¯"""
    user = f"**From {ctx.author.name}:**"
    await message.delete()
    await ctx.send(''.join((user, message, ' ¯\_(ツ)_/¯')))
