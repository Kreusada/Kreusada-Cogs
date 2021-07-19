import contextlib
import logging
import math
from datetime import datetime, timedelta

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import bold, box, humanize_number, humanize_timedelta

log = logging.getLogger("red.kreusada.advanceduptime")


class AdvancedUptime(commands.Cog):
    """
    Show [botname]'s uptime, with extra stats.
    """

    __author__ = ["Kreusada"]
    __version__ = "2.0.3"

    def __init__(self, bot):
        self.bot = bot
        self.commands_run = {}
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("advanceduptime", lambda x: self)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if await self.bot.cog_disabled_in_guild(self, ctx.guild):
            return
        if not await self.bot.ignored_channel_or_guild(ctx):
            return
        if not await self.bot.allowed_by_whitelist_blacklist(ctx.author):
            return

        command = str(ctx.command)

        if command in self.commands_run.keys():
            self.commands_run[command] += 1
            return
        self.commands_run[command] = 1

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

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

        def format_timedelta(delta: timedelta, unit: str):
            mapper = {"seconds": 1, "minutes": 60, "hours": 3600, "days": 86400}
            return humanize_number(math.floor(delta.total_seconds() / mapper[unit]))

        delta = datetime.utcnow() - self.bot.uptime
        description = f"{self.bot.user} has been up for {bold(humanize_timedelta(timedelta=delta) or 'less than one second')}.\n\n"

        embed = discord.Embed(
            title="\N{LARGE GREEN CIRCLE} Uptime Information",
            description=description,
            color=await ctx.embed_colour(),
            timestamp=datetime.now(),
        )

        data = {}
        units = ("seconds", "minutes", "hours", "days")
        for unit in units:
            data[unit] = str(format_timedelta(delta, unit))

        plural_unit = lambda x: f"{data[x]} {x[:-1]}" if data[x] == 1 else f"{data[x]} {x}"

        unit_details = "\n".join(f"+ {plural_unit(x)}" for x in units)
        embed.add_field(name="Unit Details", value=box(unit_details, lang="diff"), inline=False)

        app_info = await self.bot.application_info()
        bot_stats = {
            "users": humanize_number(len(self.bot.users)),
            "servers": humanize_number(len(self.bot.guilds)),
            "commands_available": humanize_number(len(set(self.bot.walk_commands()))),
            "owner": app_info.team.name if app_info.team else app_info.owner,
        }

        format_key = lambda x: x.replace("_", " ").capitalize()
        sorted_bot_stats = sorted(bot_stats.items(), key=lambda x: len(x[0]))

        embed.add_field(
            name="Bot Stats",
            value=box(
                "\n".join(f"{format_key(k)}: {v}" for k, v in sorted_bot_stats), lang="yaml"
            ),
            inline=False,
        )

        if self.commands_run:
            most_run_command = sorted(self.commands_run.items(), key=lambda x: x[1], reverse=True)
            format_time = lambda x: "once" if x == 1 else f"{x} times"
            command_usage = f"The most used command whilst the bot has been online is `{most_run_command[0][0]}`, which has been used {format_time(most_run_command[0][1])}."
            if len(self.commands_run) != 1:
                command_usage += f"\n\nThe least used command is `{most_run_command[-1][0]}`, which has been used {format_time(most_run_command[-1][1])}."

            embed.add_field(
                name="Command usage since this cog has been loaded",
                value=command_usage,
                inline=False,
            )

        embed.set_author(name=self.bot.user, icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    au = AdvancedUptime(bot)
    global _old_uptime
    _old_uptime = bot.get_command("uptime")
    if _old_uptime:
        bot.remove_command(_old_uptime.name)
    bot.add_cog(au)
