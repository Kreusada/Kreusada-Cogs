import discord
from redbot.core import commands, Config
from redbot.core.utils import AsyncIter
from datetime import datetime, timedelta
from .delta_utils import humanize_timedelta

class FancyUptime(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(self, identifier=59365034743, force_registration=True)
       
  def cog_unload(self):
    global _old_uptime
    if _old_uptime:
      try:
        self.bot.remove_command("uptime")
      except Exception as error:
        log.info(error)
      self.bot.add_command(_old_uptime)

  @commands.command()
  async def uptime(self, ctx: commands.Context):
      """Shows [botname]'s uptime."""
      since = ctx.bot.uptime.strftime("%A the %d of %B, %Y")
      delta = datetime.utcnow() - self.bot.uptime
      uptime_str = humanize_timedelta(timedelta=delta) or ("Less than one second")
      bot = ctx.bot.user.name
      users = len(self.bot.users)
      servers = (len(bot.guilds)
      commandscount = len(set(bot.walk_commands()))
      now = datetime.now()
      strftime = now.strftime("Today at %H:%M %p")
      e = discord.Embed(title=f":green_circle:  {bot}'s Uptime",
                        description=(
                          f"{bot} has been up since **{since}**.\n"
                          f"Therefore, it's been online for **{uptime_str}**.\n\n"
                          f"**Instance name:** {ctx.bot.user}\n"
                          f"**Instance ID:** {ctx.bot.user.id}\n"
                          f"**Current guild:** {ctx.guild}\n"
                          f"**Number of servers:** {servers}\n"
                          f"**Unique users:** {servers}\n"
                          f"**Commands processed since last restart:** {servers}\n"
                        ),
                        color=0x23fb31)
      e.set_footer(text=f"{strftime}")
      await ctx.send(embed=e)

async def setup(bot):
  fu = FancyUptime(bot)
  global _old_uptime
  _old_uptime = bot.get_command("uptime")
  if _old_uptime:
      bot.remove_command(_old_uptime.name)
  bot.add_cog(fu)
