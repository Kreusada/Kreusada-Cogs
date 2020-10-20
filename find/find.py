import discord
import random
from redbot.core import commands, checks, Config

class Find(commands.Cog):
  """Find"""
  
  def __init__(self):
    self.config = Config.get_conf(self, 200730042020, force_registration=True)
    
  @commands.group()
  @checks.admin()
  async def find(self, ctx):
    """The Matrix Development Team Index."""
    pass
  
  @find.group()
  async def repo(self, ctx):
    """Browse our Cog Creator's repositories."""
    
  @repo.group()
  async def kreusada(self, ctx):
    """Kreusada's Github Repository."""
    await ctx.send(f"https://github.com/KREUSADA/demaratus/")
    
  @repo.group()
  async def jojo(self, ctx):
    """Jojo's Github Repository."""
    await ctx.send(f"https://github.com/Just-Jojo/JojoCogs/")
    
  @repo.group()
  async def flyingkiller(self, ctx):
    """FlyingKiller147's Github Repository."""
    await ctx.send(f"https://github.com/FlyingKiller147/mybotfk/")
    
  @repo.group()
  async def adnayekken(self, ctx):
    """Adnayekken's Github Repository."""
    await ctx.send(f"Adnayekken's Github Repository is temporarily closed. :x:")
    
  @repo.group()
  async def otriux(self, ctx):
    """Otriux's Github Repository."""
    await ctx.send(f"Otriux's Github Repository has not yet been submitted!")
    
  @repo.group()
  async def titan(self, ctx):
    """The Mad Titan's Github Repository."""
    await ctx.send(f"Titan's Github Repository has not yet been submitted!")
    
  @repo.group()
  async def octavius(self, ctx):
    """Octavius' Github Repository."""
    await ctx.send(f"Octavius doesn't code anymore! :robot:")
    
  @repo.group()
  async def zagelfino(self, ctx):
    """Zagelfino's Github Repository."""
    await ctx.send(f"Zagelfino doesn't code anymore! :robot:")
    
  @find.group()
  async def documentation(self, ctx):
    """Shows the documentation for some of our bots."""
    
  @documentation.group()
  async def demaratus(self, ctx):
    """Demaratus' RTD Documentation."""
    await ctx.send(f"Demaratus Documentation: https://kreusadacogs.readthedocs.io/en/latest/\nThis documentation is scripted by Kreusada, and won't be completed until 2021 for sure.\nYou can contribute, let us know, or create a pull request on my github repo under /docs.")
  
  @documentation.group()
  async def collector(self, ctx):
    """Collector Documentation."""
    await ctx.send(f"Unfortunately, Collector does not have a documentation at this time.\nHowever, JJW has made some video guides for the Collector.\nYou can watch them here: https://www.youtube.com/watch?v=wO5JFXJZBHE&list=PLrM7-aBPjDsRVEq1UpvV-u85K06Ds7suD")
  
  @find.group()
  async def awbadges(self, ctx):
    """The Alliance War badge index."""
    
  @awbadges.group()
  async def master(self, ctx):
    """Master Alliance War Badges."""
  
  @awbadges.group()
  async def platinum(self, ctx):
    """Platinum Alliance War Badges."""
    
  @awbadges.group()
  async def gold(self, ctx):
    """Gold Alliance War Badges."""
    
  @awbadges.group()
  async def silver(self, ctx):
    """Silver Alliance War Badges."""
    
  @awbadges.group()
  async def bronze(self, ctx):
    """Bronze Alliance War Badges."""
    
  @awbadges.group()
  async def participation(self, ctx):
    """Participation Alliance War Badges."""
    
  @master.group(invoke_without_command=True)
  async def 1(self, ctx):
    """Master Rank 1 Badge."""
    await ctx.send(f"Placeholder.")
    
  @master.group(invoke_without_command=True)
  async def 2(self, ctx):
    """Master Rank 2 Badge."""
    await ctx.send(f"Placeholder.")
    
  @master.group(invoke_without_command=True)
  async def 3(self, ctx):
    """Master Rank 3 Badge."""
    await ctx.send(f"Placeholder.")
    
  @master.group(invoke_without_command=True)
  async def 20(self, ctx):
    """Master Top 20 Badge."""
    await ctx.send(f"Placeholder.")
    
  
 
