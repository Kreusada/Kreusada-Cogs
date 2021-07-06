import contextlib
import logging
from datetime import datetime

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, humanize_number, humanize_timedelta

log = logging.getLogger("red.kreusada.advanceduptime")


class AdvancedUptime(commands.Cog):
    """
    Show [botname]'s uptime, with extra stats.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.3.1"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("advanceduptime", lambda x: self)

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
        delta = datetime.utcnow() - self.bot.uptime
        uptime_str = humanize_timedelta(timedelta=delta) or (
            "Less than one second"
        )  # Thankyou Red-DiscordBot
        botname = ctx.bot.user.name
        users = humanize_number(len(self.bot.users))
        servers = humanize_number(len(self.bot.guilds))
        commands_available = humanize_number(len(set(self.bot.walk_commands())))
        app_info = await self.bot.application_info()
        owner = app_info.team.name if app_info.team else app_info.owner
        if await ctx.embed_requested():
            e = discord.Embed(
                title=f":green_circle:  {botname}'s Uptime",
                color=await ctx.embed_colour(),
                timestamp=ctx.message.created_at,
            )
            e.add_field(name=f"{botname} has been up for...", value=uptime_str, inline=False)
            e.add_field(name="Instance name:", value=ctx.bot.user, inline=True)
            e.add_field(name="Instance owner:", value=owner, inline=True)
            e.add_field(name="Number of guilds:", value=servers, inline=False)
            e.add_field(name="Unique users:", value=users, inline=False)
            e.add_field(name="Commands available:", value=commands_available, inline=False)
            e.set_thumbnail(url=ctx.bot.user.avatar_url)
            await ctx.send(embed=e)
        else:
            title = f"[{botname} has been up for {uptime_str}.]"
            msg = (
                f"Instance name: {ctx.bot.user}\n"
                f"Instance owner: {owner}\n"
                f"Number of guilds: {servers}\n"
                f"Unique users: {users}\n"
                f"Commands available: {commands_available}"
            )
            await ctx.send(box(title, lang="yaml"))
            await ctx.send(box(msg, lang="yaml"))


async def setup(bot):
    au = AdvancedUptime(bot)
    global _old_uptime
    _old_uptime = bot.get_command("uptime")
    if _old_uptime:
        bot.remove_command(_old_uptime.name)
    await au.initialize()
    bot.add_cog(au)
