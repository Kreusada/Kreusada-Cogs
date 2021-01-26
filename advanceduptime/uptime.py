import discord
from redbot.core import commands
from datetime import datetime, timedelta
from redbot.core.utils.chat_formatting import humanize_timedelta
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("AdvancedUptime", __file__)

@cog_i18n(_)
class AdvancedUptime(commands.Cog):
  """Show [botname]'s uptime, with extra stats."""
  
  def __init__(self, bot):
    self.bot = bot
    
# The following cog_unload function was modified from https://github.com/flaree/Flare-Cogs/blob/master/userinfo/userinfo.py.
# Thanks flare!
       
  def cog_unload(self):
    global _old_uptime
    if _old_uptime:
      try:
        self.bot.remove_command("uptime")
      except Exception as error:
        log.info(error)
      self.bot.add_command(_old_uptime)

  async def red_delete_data_for_user(self, **kwargs):
      """
      Nothing to delete
      """
      return

  @commands.command()
  async def uptime(self, ctx: commands.Context):
      """Shows [botname]'s uptime."""
      delta = datetime.utcnow() - self.bot.uptime
      uptime_str = humanize_timedelta(timedelta=delta) or ("Less than one second")
      botname = ctx.bot.user.name
      users = len(self.bot.users)
      servers = str(len(self.bot.guilds))
      commandsavail = len(set(self.bot.walk_commands()))
      app_info = await self.bot.application_info()
      if app_info.team: owner = app_info.team.name
      else: owner = app_info.owner
      e = discord.Embed(title=f":green_circle:  {botname}'s Uptime", color=0x59e1ac, timestamp=ctx.message.created_at)
      e.add_field(name=f"{botname} has been up for...", value=uptime_str, inline=False)
      e.add_field(name="Instance name:", value=ctx.bot.user, inline=True)
      e.add_field(name="Instance owner:", value=owner, inline=True)
      e.add_field(name="Current guild:", value=ctx.guild, inline=True)
      e.add_field(name="Number of guilds:", value=servers, inline=True)
      e.add_field(name="Unique users:", value=users, inline=True)
      e.add_field(name="Commands available:", value=commandsavail, inline=True)
      e.set_thumbnail(url=ctx.bot.user.avatar_url)
      await ctx.send(embed=e)

# The following code was modified from https://github.com/flaree/Flare-Cogs/blob/master/userinfo/userinfo.py.
# Thanks flare!

async def setup(bot):
  au = AdvancedUptime(bot)
  global _old_uptime
  _old_uptime = bot.get_command("uptime")
  if _old_uptime:
      bot.remove_command(_old_uptime.name)
  bot.add_cog(au)
