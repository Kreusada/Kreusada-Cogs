import discord
from redbot.core import commands
from typing import Union

class BackslashEmoji(commands.Cog):
  """Haven't got a backslash on your keyboard?"""
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(aliases=["backslash", "backslashemoji"])
  async def bse(self, ctx: commands.Context, emoji: Union[discord.Emoji, str]):
    """Convert a standard emoji into unicode."""
    if type(emoji) in [discord.PartialEmoji, discord.Emoji]:
    await ctx.send(''.join(('\\',emoji)))
    else:
      await ctx.send("No")
