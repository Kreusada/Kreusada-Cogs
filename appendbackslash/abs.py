import discord
from typing import Union
from redbot.core import commands, Config

class AppendBackslash(commands.Cog):
  """Haven't got a backslash on your keyboard?"""
  
  def __init__(self, bot):
    self.bot = bot
    self.config.register_user(cb=False)
    
  @commands.command(name="abs", aliases=["backslash", "backslashemoji"])
  async def appendbackslash(self, ctx: commands.Context, object_to_append: str):
    """Append a backslash to an object."""
    ota = object_to_append
    if cb is False:
      await ctx.send(''.join(('\\',ota)))
    else:
      await ctx.send(''.join(('\\',ota)))
    
  @commands.command()
  async def abstoggle(self, ctx, yes_or_no: str):
    """Toggle whether the response is sent in code block."""
    yon = yes_or_no
    if yon.startswith("yes", "y"):
      await self.config.cb.set(True)
    elif yon.startswith("no", "n"):
      await self.config.cb.set(False)
    else:
      await ctx.send("Are you wanting to toggle the output into a codeblock? Type **`yes`** or **`no`**.")
    
