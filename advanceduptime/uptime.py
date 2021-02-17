import discord
import logging

from redbot.core import commands
from datetime import datetime, timedelta
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import humanize_timedelta, box

_ = Translator("AdvancedUptime", __file__)

log = logging.getLogger("red.kreusada.advanceduptime")


@cog_i18n(_)
class AdvancedUptime(commands.Cog):
    """
    Show [botname]'s uptime, with extra stats.
    """

    __author__ = "Kreusada"
    __version__ = "1.3.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        return f"{super().format_help_for_context(ctx)}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

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
        uptime_str = humanize_timedelta(timedelta=delta) or (
            "Less than one second"
        )  # Thankyou Red-DiscordBot
        botname = ctx.bot.user.name
        users = len(self.bot.users)
        servers = str(len(self.bot.guilds))
        commands_available = len(set(self.bot.walk_commands()))
        app_info = await self.bot.application_info()
        owner = app_info.team.name if app_info.team else app_info.owner
        if await ctx.embed_requested():
            e = discord.Embed(
                title=f":green_circle:  {botname}'s Uptime",
                color=0x59E1AC,
                timestamp=ctx.message.created_at,
            )
            e.add_field(
                name=f"{botname} has been up for...", value=uptime_str, inline=False
            )
            e.add_field(name="Instance name:", value=ctx.bot.user, inline=True)
            e.add_field(name="Instance owner:", value=owner, inline=True)
            e.add_field(name="Current guild:", value=ctx.guild, inline=True)
            e.add_field(name="Number of guilds:", value=servers, inline=True)
            e.add_field(name="Unique users:", value=users, inline=True)
            e.add_field(
                name="Commands available:", value=commands_available, inline=True
            )
            e.set_thumbnail(url=ctx.bot.user.avatar_url)
            await ctx.send(embed=e)
        else:
            title = f"[{botname} has been up for {uptime_str}.]"
            msg = (
                f"Instance name: {ctx.bot.user}\n"
                f"Instance owner: {owner}\n"
                f"Current guild: {ctx.guild}\n"
                f"Number of guilds: {servers}\n"
                f"Unique users: {users}\n"
                f"Commands available: {commands_available}"
            )
            await ctx.send(box(title, lang="yaml"))
            await ctx.send(box(msg, lang="yaml"))


def setup(bot):
    au = AdvancedUptime(bot)
    global _old_uptime
    _old_uptime = bot.get_command("uptime")
    if _old_uptime:
        bot.remove_command(_old_uptime.name)
    bot.add_cog(au)
