import discord
from typing import Union
from redbot.core import commands, Config

class AppendBackslash(commands.Cog):
  """Haven't got a backslash on your keyboard?"""
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(name="abs", aliases=["backslash", "backslashemoji"])
  async def appendbackslash(self, ctx: commands.Context, object_to_append: str):
    """Append a backslash to an object."""
    ota = object_to_append
    await ctx.send(''.join(('\\',ota)))
