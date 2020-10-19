from redbot.core import commands

class Zuko(commands.Cog):
  """Zuko"""

@commands.group()
async def zuko(self, ctx, *):
  """All Zuko settings."""
  pass

@zuko.command()
async def zukosimple(self, ctx, *):
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


  

