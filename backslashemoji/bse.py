import discord
from redbot.core import commands

class BackslashEmoji(commands.Cog):
  """Haven't got a backslash on your keyboard?"""
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(aliases=["backslash", "backslashemoji"])
  async def bse(self, ctx: commands.Context, str: emoji: Union[discord.Emoji, str]):
    """Convert a standard emoji into unicode."""
    await ctx.send(''.join(('\\',emoji)))
