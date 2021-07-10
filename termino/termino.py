import asyncio
import contextlib
import datetime
from typing import Union

import discord
from redbot.core import Config, VersionInfo, commands, version_info
from redbot.core.utils.chat_formatting import box, pagify
from redbot.core.utils.predicates import MessagePredicate

from .log import log
from .mixins import CompositeMetaClass
from .utils import Utilities, default_wave

now = datetime.datetime.now().strftime("%d/%m/%Y (%H:%M:%S)")
shutdown: commands.Command = None
restart: commands.Command = None


async def reconnect_enabled(ctx: commands.Context):
    return await ctx.cog.config.reconnect()


class Termino(Utilities, commands.Cog, metaclass=CompositeMetaClass):
    """Customize bot shutdown and restart messages, with predicates, too."""

    __author__ = ["Kreusada", "Jojo#7791"]
    __dev_ids__ = [719988449867989142, 544974305445019651]
    __version__ = "2.0.2"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 89434930598345, force_registration=True)
        self.config.register_global(
            shutdown_message=f"Shutting down... {default_wave}",
            restarted_message="I have successfully restarted.",
            restarted_author=None,
            restart_message="Restarting...",
            reconnect=False,
            reconnect_message="I have reconnected.",
            announcement_channel=None,
            restart_channel=None,
            confirm_shutdown=True,
            confirm_restart=True,
        )

        self.red_ready = getattr(
            self.bot, "is_red_ready", lambda: self.bot._red_ready.is_set()
        )  # This might be changed soon
        self.startup_task = self.bot.loop.create_task(self.startup())
        self.announce_startup = self.bot.loop.create_task(self._announce_start())
        self._first_connect = False

    def cog_unload(self):
        global shutdown, restart
        if shutdown:
            try:
                self.bot.remove_command("shutdown")
            except Exception as e:
                log.info(e)
            self.bot.add_command(shutdown)
        if restart:
            try:
                self.bot.remove_command("restart")
            except Exception as e:
                log.info(e)
            self.bot.add_command(restart)
        with contextlib.suppress(KeyError):
            self.bot.remove_dev_env_value("termino")
        self.startup_task.cancel()
        self.announce_startup.cancel()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthors: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    async def initialize(self) -> None:
        for uid in self.__dev_ids__:
            if uid in self.bot.owner_ids:
                with contextlib.suppress(RuntimeError, ValueError):
                    self.bot.add_dev_env_value("termino", lambda x: self)
        conf = await self.config.all()
        if "announced" in conf.keys():
            await self.config.announced.clear()

    @commands.is_owner()
    @commands.command()
    async def restart(self, ctx: commands.Context):
        """Attempts to restart [botname]."""
        settings = await self.config.all()
        restart_message = settings["restart_message"]
        restart_conf = settings["confirm_restart"]

        message = restart_message.replace(r"{author}", ctx.author.name)
        if restart_conf:
            conf = await self.confirmation(ctx, "restart")
        if not restart_conf or conf:
            await ctx.send(message)
            log.info(f"{ctx.me.name} was restarted by {ctx.author} ({now})")
            await self.config.restart_channel.set(ctx.channel.id)
            await self.config.restarted_author.set(ctx.author.name)
            try:
                await asyncio.wait_for(self._send_announcement(shutdown=False), timeout=15.0)
            except asyncio.TimeoutError:
                pass
            return await self.bot.shutdown(restart=True)
        else:
            await ctx.send("I will not be restarting.")

    @commands.is_owner()
    @commands.command()
    async def shutdown(self, ctx: commands.Context):
        """Shuts down [botname]."""
        settings = await self.config.all()
        shutdown_message = settings["shutdown_message"]
        shutdown_conf = settings["confirm_shutdown"]

        message = shutdown_message.replace(r"{author}", ctx.author.name)
        if shutdown_conf:
            conf = await self.confirmation(ctx, "shutdown")
        if not shutdown_conf or conf:
            await ctx.send(message)
            log.info(f"{ctx.me.name} was shutdown by {ctx.author} ({now})")
            try:
                await asyncio.wait_for(self._send_announcement(), timeout=15.0)
            except asyncio.TimeoutError:
                pass
            return await self.bot.shutdown(restart=False)
        else:
            await ctx.send("I will not be shutting down.")

    @commands.group()
    @commands.is_owner()
    async def terminoset(self, ctx: commands.Context):
        """Settings for the shutdown and restart commands."""

    @terminoset.group(name="shutdown", aliases=["shut"], invoke_without_command=True)
    async def terminoset_shutdown(self, ctx: commands.Context, *, shutdown_message: str):
        """
        Set and adjust the shutdown message.

        You can use `{author}` in your message to send the invokers display name.

        Type `none` to reset it
        """
        if shutdown_message.lower() == "none":
            shutdown_message = None
        msg = shutdown_message or f"Shutting down... {default_wave}"
        await self.config.shutdown_message.set(msg)
        set_reset = "set" if shutdown_message else "reset"
        await ctx.send(f"Shutdown message has been {set_reset}.")

    @terminoset_shutdown.command(name="conf")
    async def terminoset_shutdown_conf(self, ctx: commands.Context, true_or_false: bool):
        """Toggle whether shutdowns confirm before shutting down."""
        await self.config.confirm_shutdown.set(true_or_false)
        grammar = "not" if not true_or_false else "now"
        await ctx.send(f"Shutdowns will {grammar} confirm before shutting down.")

    @terminoset.group(name="restart", aliases=["res"], invoke_without_command=True)
    async def terminoset_restart(self, ctx: commands.Context, *, restart_message: str):
        """
        Set and adjust the restart message.

        You can use `{author}` in your message to send the invokers display name.

        Type `none` to reset it
        """
        if restart_message.lower() == "none":
            restart_message = None
        msg = restart_message or "Restarting..."
        await self.config.restart_message.set(msg)
        set_reset = "set" if restart_message else "reset"
        await ctx.send("Restart message has been {set_reset}.")

    @terminoset_restart.command(name="conf")
    async def terminoset_restart_conf(self, ctx: commands.Context, true_or_false: bool):
        """Toggle whether restarts confirm before restarting."""
        await self.config.confirm_restart.set(true_or_false)
        grammar = "not" if not true_or_false else "now"
        await ctx.send(f"Restarts will {grammar} confirm before shutting down.")

    @terminoset_restart.command(name="restartedmessage", aliases=["resmsg"], usage="<message>")
    async def terminoset_restarted_message(self, ctx: commands.Context, *, restarted_message: str):
        """Set the message to be sent after restarting.

        Type `none` to reset it
        """
        if restarted_message.lower() == "none":
            restarted_message = None
        msg = restarted_message or "I have successfully restarted."
        set_reset = "set" if restarted_message else "reset"
        await self.config.restarted_message.set(msg)
        await ctx.send(f"Restarted message {set_reset}.")

    @terminoset.command(name="announcement")
    async def terminoset_announcement_channel(
        self, ctx: commands.Context, channel: Union[discord.TextChannel, None]
    ):
        """Set the channel where announcements will be sent to when the bot goes online/offline

        Type `none` to clear it
        """
        announcement = await self.config.announcement_channel()
        if all([not announcement, not channel]):
            return await ctx.send("The announcement channel is not set.")
        to_set = channel.id if isinstance(channel, discord.TextChannel) else channel
        await self.config.announcement_channel.set(to_set)
        msg = "The channel has been reset."
        if isinstance(channel, discord.TextChannel):
            msg = f"The channel is now set to {channel.name}."
        await ctx.send(msg)

    @terminoset.command(name="reconnect")
    async def terminoset_reconnect(self, ctx: commands.Context, true_or_false: bool):
        """Announce when the bot has reconnected"""
        await self.config.reconnect.set(true_or_false)
        grammar = "now" if true_or_false else "not"
        await ctx.send(f"Termino will {grammar} send a message when the bot reconnects")

    @terminoset.command(name="reconnectmessage")
    @commands.check(reconnect_enabled)
    async def termionset_reconnect_message(self, ctx: commands.Context, *, message: str):
        """Set the message the bot will send on reconnect

        Type `none` to reset it
        """
        if message.lower() == "none":
            message = None
        message = message or "I have reconnected."
        set_reset = "set" if message else "reset"
        await self.config.reconnect_message.set(message)
        await ctx.send(f"The reconnect message has been {set_reset}")

    @terminoset.command()
    async def settings(self, ctx: commands.Context):
        """See the current settings for termino."""
        config = await self.config.all()
        footer = False
        for x in [config["restart_message"], config["shutdown_message"]]:
            if "{author}" in x:
                footer = True
        reconnect = config["reconnect"]
        reconnect_msg = f"Reconnect message: {config['reconnect_message']}\n" if reconnect else ""
        message = (
            f"Announcement channel: {config['announcement_channel']}\n"
            f"Shutdown message: {config['shutdown_message']}\n"
            f"Shutdown confirmation: {config['confirm_shutdown']}\n\n"
            f"Reconnect announcements: {reconnect}\n"
            f"{reconnect_msg}"
            f"Restart message: {config['restart_message']}\n"
            f"Restart confirmation: {config['confirm_restart']}\n"
            f"Restarted message: {config['restarted_message']}\n"
            f"\t- NOTE: This message will be sent in the invoked channel when a successful restart has occured.\n\n"
        )
        if footer:
            message += "{author} will be replaced with the display name of the invoker."
        for page in pagify(message, delims=["\n"]):
            await ctx.send(box(page, lang="yaml"))


async def setup(bot):
    cog = Termino(bot)
    global shutdown
    global restart

    # `bot.remove_command` will attempt to remove a command and return it back
    # if no command with the name given exists it will return `None`
    # So we can skip a large chunk of this code for that reason
    shutdown = bot.remove_command("shutdown")
    restart = bot.remove_command("restart")
    await cog.initialize()
    bot.add_cog(cog)
