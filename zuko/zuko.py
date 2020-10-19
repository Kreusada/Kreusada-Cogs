from redbot.core import commands, Config
#import discord

class Zuko(commands.Cog):
  """Zuko"""

def __init__(self, bot):
  self.bot = bot
  self.config = Config.get_conf(
    self,
    identifier=
    force_registration = True,
  )

#@commands.group()
#async def zuko(self, ctx):
#  """All Zuko settings."""
#  pass

@commands.command()
async def zukosimple(self, ctx):
  """Simple test response from Zuko."""
  await ctx.send('**You got the `coding` just right. :white_check_mark:.**')

#@commands.group()
#async def zukosubcats(self, ctx, *):
#  """Testing sub-categories."""
#  pass

#@zukosubcats.command():
#  async def subcat(self, ctx, *):
#    """Here should be your sub category. *Should be*."""
#    await ctx.send('Subcategory command **successful**. :sparkles:')


  

