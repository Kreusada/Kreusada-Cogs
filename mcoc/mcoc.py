from redbot.core import commands, checks, Config
import discord
import random
from .mdtembed import Embed
from .featureds import FEATUREDS

class Mcoc(commands.Cog):
  """Mcoc"""
  
  def __init__(self):
    self.config = Config.get_conf(self, 200730042020, force_registration=True)
    
  @commands.group(invoke_without_command=True)
  async def crystal(self, ctx):
    """Chooses a random champion from MCOC."""
    author = ctx.message.author
    data = Embed.create(self, ctx, title='Participation Badge :trophy:')
    image = (random.choice(FEATUREDS))
    name = ctx.author.name
    data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    data.set_image(url=image)
    await ctx.send(embed=data)
    
    
#    await ctx.send(random.choice(CHAMPS))
      
