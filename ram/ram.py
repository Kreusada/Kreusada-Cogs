import psutil
from redbot.core import commands
from redbot.core.utils.chat_formatting import box as b

RAMU = "Random Access Memory used: "

class RAM(commands.Cog):
  """Get [botname]'s ram."""

  __author__ = ["Kreusada"]
  __version__ = "1.0.0
  
  def __init__(self, bot):
    self.bot = bot

  def format_help_for_context(self, ctx: commands.Context) -> str:
    """Thanks Sinbad."""
    return f"{super().format_help_for_context(ctx)}\nAuthor: {self.__author__}\nVersion: {self.__version__}"
    
  @commands.command()
  @commands.is_owner()
  async def ram(self, ctx):
    """Get [botname]'s ram."""
    await ctx.send(b(text=f'{RAMU}[{psutil.virtual_memory()[2]}%]', lang='css'))

def setup(bot):
    bot.add_cog(RAM(bot))
