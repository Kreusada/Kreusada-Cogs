import discord
from redbot.core import Config, commands
from redbot.core.utils import AsyncIter

class PingOveride(commands.Cog):
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
  async def pingset(self, ctx, *, response: str):
    """
    Set your custom ping message.
    You can use {name} to represent the author.
    """
    if '{name}' in response:
      name = ctx.author
      await self.config.response.set(response)
      await ctx.send("Running `{}ping` will now respond with: {}".format(ctx.clean_prefix, response.replace('{name}', "`user`")))
    else:
      await self.config.response.set(response)
      await ctx.send(f"Running `{ctx.clean_prefix}ping` will now respond with: **{response}**")

  @commands.is_owner()  
  @commands.command()
  async def pingsettings(self, ctx):
    """Shows the current ping settings."""
    response = await self.config.response()
    if '{name}' in response:
      await ctx.send(
        f"The current ping response is **{response}**.\n"
        "**{name}** will represent the command author."
      )
    else:
      await ctx.send(f"The current ping response is **{response}**.")
    
  @commands.command()
  async def ping(self, ctx):
    """Pong. Or not?"""
    resp = await self.config.response()
    if resp is None:
      response = "Pong."
    elif '{name}' in resp:
      response = resp.replace('{name}', ctx.author.name)
    else:
      response = resp
    await ctx.send(response)

async def setup(bot):
    if discord.version_info <= (1, 4):
        raise CogLoadError("This cog requires d.py 1.4+ to work.")
    cping = PingOveride(bot)
    global _old_ping
    _old_ping = bot.get_command("ping")
    if _old_ping:
        bot.remove_command(_old_ping.name)
    bot.add_cog(cping)
