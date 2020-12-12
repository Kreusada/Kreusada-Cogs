import discord
from redbot.core import bank, commands
from redbot.core.utils import AsyncIter

class CustomPing(commands.Cog):
  """Custom ping message."""
  
  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(self, identifier=59365034743, force_registration=True)
    self.config.register_global(response=None)
    
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
  async def pingset(self, ctx, *, response: str = None):
    """Set your custom ping message."""
    if response is None:
      msg = await self.config.response()
      if msg is None:
        await ctx.send(f"Running `{ctx.clean_prefix}ping` will currently respond with: ```{msg}```")
        return
      await self.config.response.set(response)
      await ctx.send(f"Running `{ctx.clean_prefix}ping` will respond with: ```{msg}```")
      
  @commands.command()
  async def ping(self, ctx):
    """Pong."""
    resp = await self.config.response()
    if resp = None:
      response = "Pong."
    else:
      response = resp
    await ctx.send(response)
