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

  def get(self, key, id=None, raw: bool = False) -> Union[int, str]:
      if id is None:
          query = SELECT_TEMP_GLOBAL
          condition = {"event": key}
      else:
          query = SELECT_TEMP_SINGLE
          condition = {"event": key, "guild_id": id}
      output = threadexec(self.cursor.execute, query, condition)
      result = list(output)
      if raw:
          return result[0][0] if result else 0
      return humanize_number(result[0][0] if result else 0)
              
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
      bot = ctx.bot.user
      guild = ctx.guild
      users = len(self.bot.users)
      servers = str(len(self.bot.guilds))
      commandsavail = len(set(self.bot.walk_commands()))
      commands_count = self.get("processed_commands")
      now = datetime.now()
      strftime = now.strftime("Today at %H:%M %p")
      e = discord.Embed(title=f":green_circle:  {bot}'s Uptime",
                        description=(
                          f"**{bot.name}** has been up since **{since}**.\n"
                          f"Therefore, it's been online for **{uptime_str}**."
                        ),
                        color=0x59e1ac)
      e.add_field(name="Instance name:", value=bot.name, inline=True)
      e.add_field(name="Instance ID:", value=bot.id, inline=True)
      e.add_field(name="Current guild:", value=guild, inline=True)
      e.add_field(name="Number of servers:", value=servers, inline=True)
      e.add_field(name="Unique users:", value=users, inline=True)
      e.add_field(name="Commands available:", value=commandsavail, inline=True)
      e.add_field(name="Commands count:", value=commands_count, inline=True)
      e.set_footer(text=f"{strftime}")
      await ctx.send(embed=e)

async def setup(bot):
  fu = FancyUptime(bot)
  global _old_uptime
  _old_uptime = bot.get_command("uptime")
  if _old_uptime:
      bot.remove_command(_old_uptime.name)
  bot.add_cog(fu)
