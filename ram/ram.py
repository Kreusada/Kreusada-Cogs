import discord
import psutil
from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import bold as b, box

RAMU = "Random Access Memory used: "

class RAM(commands.Cog):
  """Get your bot's ram."""
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  async def ram(self, ctx):
    await ctx.send(box(text=f'{RAMU}[{psutil.virtual_memory()[2]}%]', lang='css'))

def setup(bot):
    bot.add_cog(RAM(bot))
