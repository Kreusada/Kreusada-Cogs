from redbot.core import commands, Config
import random

class RandomNitroBooster(commands.Cog):
  """Get a random nitro booster."""
  
  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(
        self, identifier=176070082584248320, force_registration=True
    )
    self.config.register_guild()
    
  @commands.command()
  async def randomnitro(self, ctx):
    guild = ctx.guild
    nitroer = guild.premium_subscribers
    nitroerrand = random.choice(nitroer)
    await ctx.send(f"{nitroerrand.name}")
  
