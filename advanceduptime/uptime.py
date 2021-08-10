import contextlib
import logging
import math
from datetime import datetime, timedelta

try:
    import psutil
except ModuleNotFoundError:
    psutil = False

import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import bold, box, humanize_number, humanize_timedelta

log = logging.getLogger("red.kreusada.advanceduptime")

default_settings = {
    "show_bot_stats": True,
    "show_latency_stats": True,
    "show_usage_stats": True,
    "show_system_uptime_stats": bool(psutil),
}


class AdvancedUptime(commands.Cog):
    """
    Show [botname]'s uptime, with extra stats.
    """

    __author__ = ["Kreusada"]
    __version__ = "3.1.0"

    def __init__(self, bot):
        self.bot = bot
        self.commands_run = {}
        self.settings = {}
        self.config = Config.get_conf(self, 4589035903485, True)
        self.config.register_global(**default_settings)
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

        if not self.settings["show_usage_stats"]:
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

    async def initialize(self):
        self.settings = await self.config.all()

    def format_timedelta(self, delta: timedelta):
        def clean_format(delta: timedelta, unit: str):
            mapper = {"seconds": 1, "minutes": 60, "hours": 3600, "days": 86400}
            return humanize_number(math.floor(delta.total_seconds() / mapper[unit]))

        data = {}
        units = ("seconds", "minutes", "hours", "days")
        for unit in units:
            data[unit] = str(clean_format(delta, unit))

        plural_unit = lambda x: f"{data[x]} {x[:-1]}" if data[x] == 1 else f"{data[x]} {x}"
        unit_details = "\n".join(f"+ {plural_unit(x)}" for x in units)

        return unit_details

    @commands.group()
    async def uptimeset(self, ctx: commands.Context):
        """Settings for the uptime command."""

    @uptimeset.command(name="botstats")
    async def uptimeset_botstats(self, ctx: commands.Context, true_or_false: bool):
        """Toggles whether bot stats are shown in the uptime command."""
        word = "enabled" if true_or_false else "disabled"
        await ctx.send("Bot stats {}.".format(word))
        self.settings["show_bot_stats"] = true_or_false
        await self.config.show_bot_stats.set(true_or_false)

    @uptimeset.command(name="latencystats")
    async def uptimeset_latencystats(self, ctx: commands.Context, true_or_false: bool):
        """Toggles whether latency stats are shown in the uptime command."""
        word = "enabled" if true_or_false else "disabled"
        await ctx.send("Latency stats {}.".format(word))
        self.settings["show_latency_stats"] = true_or_false
        await self.config.show_latency_stats.set(true_or_false)

    @uptimeset.command(name="sysuptime")
    async def uptimeset_sysuptime(self, ctx: commands.Context, true_or_false: bool):
        """Toggles whether system uptime stats are shown in the uptime command."""
        if all([true_or_false, not psutil]):
            return await ctx.send("This setting requires the `psutil` library to be installed.")
        word = "enabled" if true_or_false else "disabled"
        await ctx.send("System uptime stats {}.".format(word))
        self.settings["show_system_uptime_stats"] = true_or_false
        await self.config.show_system_uptime_stats.set(true_or_false)

    @uptimeset.command(name="settings", aliases=["showsettings"])
    async def uptimeset_settings(self, ctx: commands.Context):
        """Shows the settings for the uptime command."""
        format_key = lambda x: x.replace("_", " ").capitalize()
        settings = await self.config.all()
        message = "\n".join(
            f"{bold(format_key(setting))}: {settings[setting]}"
            for setting in sorted(default_settings.keys(), key=len)
        )
        await ctx.send(message)

    @uptimeset.command(name="usagestats")
    async def uptimeset_usagestats(self, ctx: commands.Context, true_or_false: bool):
        """Toggles whether usage stats are shown in the uptime command."""
        word = "enabled" if true_or_false else "disabled"
        message = "Usage stats {}.".format(word)
        if true_or_false:
            message += (
                " Command usage will not be tracked with this cog whilst this setting is disabled."
            )
        await ctx.send(message)
        self.settings["show_usage_stats"] = true_or_false
        await self.config.show_usage_stats.set(true_or_false)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def uptime(self, ctx: commands.Context):
        """Shows [botname]'s uptime."""
        delta = datetime.utcnow() - self.bot.uptime
        description = f"{self.bot.user} has been up for {bold(humanize_timedelta(timedelta=delta) or 'less than one second')}."

        embed = discord.Embed(
            title="\N{LARGE GREEN CIRCLE} Uptime Information",
            color=await ctx.embed_colour(),
            timestamp=datetime.now(),
        )

        unit_details = self.format_timedelta(delta)
        embed.add_field(
            name="Bot Uptime Details",
            value=description + box(unit_details, lang="diff"),
            inline=False,
        )

        if self.settings["show_system_uptime_stats"]:
            delta = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
            description = f"The bot's system has been up for {bold(humanize_timedelta(timedelta=delta)  or 'less than one second')}."

            unit_details = self.format_timedelta(delta)
            embed.add_field(
                name="System Uptime Details",
                value=description + box(unit_details, lang="diff"),
                inline=False,
            )

        if self.settings["show_bot_stats"]:
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

        if self.settings["show_latency_stats"]:
            value = "Bot latency: {}ms".format(str(round(self.bot.latency * 1000, 2)))
            for shard, time in self.bot.latencies:  # Thanks aika
                value += f"\nShard {shard+1}/{len(self.bot.latencies)}: {round(time * 1000)}ms"

            embed.add_field(
                name="Shard and Latency Stats",
                value=box(value, lang="yaml"),
                inline=False,
            )

        if self.settings["show_usage_stats"]:
            if self.commands_run:
                most_run_command = sorted(
                    self.commands_run.items(), key=lambda x: x[1], reverse=True
                )
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


async def setup(bot):
    au = AdvancedUptime(bot)
    global _old_uptime
    _old_uptime = bot.get_command("uptime")
    if _old_uptime:
        bot.remove_command(_old_uptime.name)
    await au.initialize()
    bot.add_cog(au)
