import discord
from redbot.core import Config, commands

from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("PingOverride", __file__)

@cog_i18n(_)
class PingOverride(commands.Cog):
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
  @commands.guild_only()
  async def pingset(self, ctx, *, response: str):
    """
    Set your custom ping message.
    
    You can use {name} to represent the author.
    You can use {nick} to represent the author's nickname.
    """
    if '{name}' in response:
      name = ctx.author
      await self.config.response.set(response)
      await ctx.send("Running `{}ping` will now respond with: {}".format(ctx.clean_prefix, response.replace('{name}', "(user's name)")))
    elif '{nick}' in response:
      nick = ctx.author.nick
      await self.config.response.set(response)
      await ctx.send("Running `{}ping` will now respond with: {}".format(ctx.clean_prefix, response.replace('{nick}', "(user's nickname)")))
    else:
      await self.config.response.set(response)
      await ctx.send(f"Running `{ctx.clean_prefix}ping` will now respond with: **{response}**")

  @commands.is_owner()  
  @commands.command()
  @commands.guild_only()
  async def pingsettings(self, ctx):
    """Shows the current ping settings."""
    response = await self.config.response()
    if '{name}' in response:
      await ctx.send(
        f"The current ping response is: **{response}**.\n"
        "**{name}** will represent the command author."
      )
    if '{nick}' in response:
      await ctx.send(
        f"The current ping response is: **{response}**.\n"
        "**{nick}** will represent the command author's nickname."
      )
    else:
      await ctx.send(f"The current ping response is: **{response}**.")
    
  @commands.command()
  async def ping(self, ctx):
    """Pong. Or not?"""
    resp = await self.config.response()
    if ctx.channel == ctx.author.dm_channel:
      nick = ctx.author.name
    else:
      if ctx.author.nick is None:
        nick = ctx.author.name
      else:
        nick = ctx.author.nick
      if resp is None:
        response = "Pong."
      elif '{name}' in resp:
        response = resp.replace('{name}', ctx.author.name)
      elif '{nick}' in resp:
        response = resp.replace('{nick}', nick)
      else:
        response = resp
      await ctx.send(response)

async def setup(bot):
    cping = PingOverride(bot)
    global _old_ping
    _old_ping = bot.get_command("ping")
    if _old_ping:
        bot.remove_command(_old_ping.name)
    bot.add_cog(cping)
