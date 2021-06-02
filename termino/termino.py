import asyncio
import contextlib
import datetime
import logging
from random import expovariate

import discord
from redbot.core import commands, Config, version_info, VersionInfo
from redbot.core.utils.chat_formatting import box, pagify
from redbot.core.utils.predicates import MessagePredicate

default_wave = "\N{WAVING HAND SIGN}\N{EMOJI MODIFIER FITZPATRICK TYPE-3}"
log = logging.getLogger("red.kreusada.termino")
now = datetime.datetime.now().strftime("%d/%m/%Y (%H:%M:%S)")
shutdown: commands.Command = None
restart: commands.Command = None


class Termino(commands.Cog):
    """Customize bot shutdown and restart messages, with predicates, too."""

    __author__ = ["Kreusada"]
    __version__ = "1.0.3"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 89434930598345, force_registration=True)
        self.config.register_global(
            shutdown_message=f"Shutting down... {default_wave}",
            restarted_message="I have successfully restarted.",
            restarted_author=None,
            restart_message="Restarting...",
            restart_channel=None,
            confirm_shutdown=True,
            confirm_restart=True,
        )
        self.startup_task = self.bot.loop.create_task(self.startup())

    def cog_unload(self):
        global shutdown
        global restart
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
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("termino")
        # This is worse case scenario but still important to check for
        if self.startup_task:
            self.startup_task.cancel()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    async def startup(self):
        if version_info >= VersionInfo.from_str("3.2.0"):
            await self.bot.wait_until_red_ready()
        else:
            await self.bot.wait_until_ready()
        conf = await self.config.all()
        maybe_channel = conf.get("restart_channel", None)
        await self.config.restart_channel.clear()
        # Using the walrus operator we can check if the channel is originally None
        # Or that we cannot find that channel
        if maybe_channel is None or (ch := self.bot.get_channel(maybe_channel)) is None:
            return
        author = await self.config.restarted_author()
        try:
            await ch.send(conf["restarted_message"].replace(r"{author}", author))
        except discord.Forbidden as e:
            log.info("Unable to send a confirmation message to the restart channel")
            log.debug(f"Unable to send a message to channel: {ch.guild} ({ch.guild.id})", exc_info=e)

    async def confirmation(self, ctx: commands.Context, _type: str):
        await ctx.send(f"Are you sure you want to {_type} {ctx.me.name}? (yes/no)")
        with contextlib.suppress(asyncio.TimeoutError):
            pred = MessagePredicate.yes_or_no(ctx, user=ctx.author)
            await ctx.bot.wait_for("message", check=pred, timeout=60)
            return pred.result
        return False

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("termino", lambda x: self)

    @commands.is_owner()
    @commands.command()
    async def restart(self, ctx: commands.Context):
        """Attempts to restart [botname]."""
        restart_message = await self.config.restart_message()
        restart_conf = await self.config.confirm_restart()
        message = restart_message.replace(r"{author}", ctx.author.name)
        if restart_conf:
            conf = await self.confirmation(ctx, "restart")
        if not restart_conf or conf:
            await ctx.send(message)
            log.info(f"{ctx.me.name} was restarted by {ctx.author} ({now})")
            await self.config.restart_channel.set(ctx.channel.id)
            await self.config.restarted_author.set(ctx.author.name)
            return await self.bot.shutdown(restart=True)
        else:
            await ctx.send("I will not be restarting.")

    @commands.is_owner()
    @commands.command()
    async def shutdown(self, ctx: commands.Context):
        """Shuts down [botname]."""
        shutdown_message = await self.config.shutdown_message()
        shutdown_conf = await self.config.confirm_shutdown()
        message = shutdown_message.replace(r"{author}", ctx.author.name)
        if shutdown_conf:
            conf = await self.confirmation(ctx, "shutdown")
        if not shutdown_conf or conf:
            await ctx.send(message)
            log.info(f"{ctx.me.name} was shutdown by {ctx.author} ({now})")
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

        You can use `{author}` in your message to send the invokers display name."""
        await ctx.invoke(self.terminoset_shutdown_message, shutdown_message=shutdown_message)

    @terminoset_shutdown.command(name="conf")
    async def terminoset_shutdown_conf(self, ctx: commands.Context, true_or_false: bool):
        """Toggle whether shutdowns confirm before shutting down."""
        await self.config.confirm_shutdown.set(true_or_false)
        grammar = "not" if not true_or_false else "now"
        await ctx.send(f"Shutdowns will {grammar} confirm before shutting down.")

    @terminoset_shutdown.command(name="message", hidden=True)
    async def terminoset_shutdown_message(self, ctx: commands.Context, *, shutdown_message: str):
        """Set the shutdown message."""
        await self.config.shutdown_message.set(shutdown_message)
        await ctx.send("Shutdown message set.")

    @terminoset.group(name="restart", aliases=["res"], invoke_without_command=True)
    async def terminoset_restart(self, ctx: commands.Context, *, restart_message: str):
        """
        Set and adjust the restart message.

        You can use `{author}` in your message to send the invokers display name."""
        await ctx.invoke(self.terminoset_restart_message, restart_message=restart_message)

    @terminoset_restart.command(name="conf")
    async def terminoset_restart_conf(self, ctx: commands.Context, true_or_false: bool):
        """Toggle whether restarts confirm before restarting."""
        await self.config.confirm_restart.set(true_or_false)
        grammar = "not" if not true_or_false else "now"
        await ctx.send(f"Restarts will {grammar} confirm before shutting down.")

    @terminoset_restart.command(name="message", hidden=True)
    async def terminoset_restart_message(self, ctx: commands.Context, *, restart_message: str):
        """Set the restart message."""
        await self.config.restart_message.set(restart_message)
        await ctx.send("Restart message set.")

    @terminoset_restart.command(name="restartedmessage", aliases=["resmsg"], usage="<message>")
    async def terminoset_restarted_message(self, ctx: commands.Context, *, restarted_message: str):
        """Set the message to be sent after restarting."""
        await self.config.restarted_message.set(restarted_message)
        await ctx.send("Restarted message set.")

    @terminoset.command()
    async def settings(self, ctx: commands.Context):
        """See the current settings for termino."""
        config = await self.config.all()
        footer = False
        for x in [config["restart_message"], config["shutdown_message"]]:
            if "{author}" in x:
                footer = True
        message = (
            f"Shutdown message: {config['shutdown_message']}\n"
            f"Shutdown confirmation: {config['confirm_shutdown']}\n\n"
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
