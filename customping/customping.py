import discord
from redbot.core import Config, commands
from redbot.core.utils import AsyncIter

class CustomPing(commands.Cog):
  """Custom ping message."""
  
  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(self, identifier=59365034743, force_registration=True)
    self.config.register_global(response="Pong.")
    
  def cog_unload(self):
      global _old_ping
      if _old_ping:
          try:
              self.bot.remove_command("ping")
          except Exception as error:
              log.info(error)
          self.bot.add_command(_old_ping)
    
  @commands.is_owner()  
  @commands.command()
  async def pingset(self, ctx, *, response: str = "Pong."):
    """Set your custom ping message."""
    await self.config.response.set(response)
    response = await self.config.response()
    await ctx.send(f"Running `{ctx.clean_prefix}ping` will respond with: ```diff +{response}```")
      
  @commands.command()
  async def ping(self, ctx):
    """Pong."""
    resp = await self.config.response()
    if resp is None:
      response = "Pong."
    else:
      response = resp
    await ctx.send(response)

async def setup(bot):
    if discord.version_info <= (1, 4):
        raise CogLoadError("This cog requires d.py 1.4+ to work.")
    cping = CustomPing(bot)
    global _old_ping
    _old_ping = bot.get_command("ping")
    if _old_ping:
        bot.remove_command(_old_ping.name)
    bot.add_cog(cping)
