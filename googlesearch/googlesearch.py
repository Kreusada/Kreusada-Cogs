import discord
from redbot.core import commands

class GoogleSearch(commands.Cog):
  """Search google with simplified URLs."""
  
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command()
  async def google(self, ctx, *search):
    """Get a google URL."""
    search = [escape(s, mass_mentions=True) for s in search if s]
    if len(search) < 2:
        await ctx.send(_("Not enough options to pick from."))
    else:
        await ctx.send(search)
