import discord
from redbot.core import commands, Config
from redbot.core.utils import AsyncIter
from datetime import datetime, timedelta
from .delta_utils import humanize_timedelta

class FancyUptime(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.config = Config.get_conf(self, identifier=59465034743, force_registration=True)
       
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
      bot = ctx.bot.user
      botname = ctx.bot.user.name
      guild = ctx.guild
      users = len(self.bot.users)
      servers = str(len(self.bot.guilds))
      commandsavail = len(set(self.bot.walk_commands()))
      now = datetime.now()
      strftime = now.strftime("Today at %H:%M %p")
      e = discord.Embed(title=f":green_circle:  {botname}'s Uptime",
                        description=(
                          f"**{botname}** has been up since **{since}**.\n"
                          f"Therefore, it's been online for **{uptime_str}**."
                        ),
                        color=0x59e1ac)
      e.add_field(name="Instance name:", value=bot.name, inline=True)
      e.add_field(name="Current guild:", value=guild, inline=True)
      e.add_field(name="Number of servers:", value=servers, inline=True)
      e.add_field(name="Unique users:", value=users, inline=True)
      e.add_field(name="Commands available:", value=commandsavail, inline=True)
      e.set_footer(text=f"{strftime}")
      await ctx.send(embed=e)

async def setup(bot):
  fu = FancyUptime(bot)
  global _old_uptime
  _old_uptime = bot.get_command("uptime")
  if _old_uptime:
      bot.remove_command(_old_uptime.name)
  bot.add_cog(fu)
