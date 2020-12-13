import discord
from redbot.core import commands
from redbot.core.utils import AsyncIter
from datetime import datetime, timedelta
from .delta_utils import humanize_timedelta

class FancyUptime(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
       
  def cog_unload(self):
    global _old_uptime
    if _old_uptime:
      try:
        self.bot.remove_command("uptime")
      except Exception as error:
        log.info(error)
      self.bot.add_command(_old_uptime)

  @commands.Cog.listener()
  async def on_command(self, ctx: commands.Context):
    self.upsert(
    rgetattr(ctx, "guild.id", rgetattr(ctx, "channel.id", -1)), "processed_commands"
    )

  @commands.command()
  async def uptime(self, ctx: commands.Context):
      """Shows [botname]'s uptime."""
      since = ctx.bot.uptime.strftime("%A the %d of %B, %Y")
      delta = datetime.utcnow() - self.bot.uptime
      uptime_str = humanize_timedelta(timedelta=delta) or ("Less than one second")
      bot = ctx.bot.user.name
      e = discord.Embed(title=f":green_circle: {bot}'s Uptime",
                        description=(
                          f"{bot} has been up since **{since}**.\n"
                          f"Therefore, it's been online for **{uptime_str}**.\n\n"
                          f"**Bot Identification:** {ctx.bot.user.id}\n"
                        )
                       )
      await ctx.send(embed=e)

async def setup(bot):
  fu = FancyUptime(bot)
  global _old_uptime
  _old_uptime = bot.get_command("uptime")
  if _old_uptime:
      bot.remove_command(_old_uptime.name)
  bot.add_cog(fu)
