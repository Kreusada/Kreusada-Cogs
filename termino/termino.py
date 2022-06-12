import asyncio
from typing import Literal, Optional

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.utils import get_end_user_data_statement
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.predicates import MessagePredicate

from .log import log

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)

OLD_RESTART_COMMAND: commands.Command = None
OLD_SHUTDOWN_COMMAND: commands.Command = None
DEFAULT_WAVE: str = "\N{WAVING HAND SIGN}\N{EMOJI MODIFIER FITZPATRICK TYPE-3}"

FORMAT_MAPPING = {
    "$name": lambda user: user.name,
    "$discriminator": lambda user: str(user.discriminator),
    "$id": lambda user: str(user.id),
    "$display_name": lambda user: user.display_name,
    "$mention": lambda user: user.mention,
}


class Termino(commands.Cog):
    """Customize shutdown and restart messages, with the ability to add confirmation messages."""

    __version__ = "3.0.6"
    __author__ = "Kreusada"

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(self, 89434930598345, force_registration=True)
        self.config.register_global(
            shutdown_message=f"Shutting down... {DEFAULT_WAVE}",
            restart_message="Restarting...",
            shutdown_confirmation_message=False,
            restart_confirmation_message=False,
        )

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    def cog_unload(self) -> None:
        global OLD_RESTART_COMMAND, OLD_SHUTDOWN_COMMAND
        if OLD_SHUTDOWN_COMMAND:
            try:
                self.bot.remove_command("shutdown")
            except Exception as e:
                log.info(e)
            self.bot.add_command(OLD_SHUTDOWN_COMMAND)
        if OLD_RESTART_COMMAND:
            try:
                self.bot.remove_command("restart")
            except Exception as e:
                log.info(e)
            self.bot.add_command(OLD_RESTART_COMMAND)

    @commands.group()
    @commands.is_owner()
    async def terminoset(self, ctx: commands.Context) -> None:
        """Configure Termino messages."""
        pass

    @terminoset.group(name="restart")
    async def terminoset_restart(self, ctx: commands.Context) -> None:
        """Set Termino's restart settings."""

    @terminoset.group(name="shutdown")
    async def terminoset_shutdown(self, ctx: commands.Context) -> None:
        """Set Termino's shutdown settings."""

    def format_message(self, author: discord.Member, message: str) -> str:
        for key, value in FORMAT_MAPPING.items():
            message = message.replace(key, value(author))
        return message

    async def maybe_confirm(
        self, ctx: commands.Context, *, type: Literal["shutdown", "restart"]
    ) -> bool:
        config_obj = getattr(self.config, "{type}_confirmation_message".format(type=type))
        message = await config_obj()
        if not message:
            return True
        await ctx.send(self.format_message(ctx.author, message))
        pred = MessagePredicate.yes_or_no(ctx, user=ctx.author)
        try:
            await self.bot.wait_for("message", check=pred, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond, assuming no.")
            return False
        else:
            if not pred.result:
                await ctx.send("Cancelling {type}.".format(type=type))
                return False
            return True

    @terminoset_restart.command(name="message")
    async def terminoset_restart_message(self, ctx: commands.Context, *, message: str) -> None:
        """Set Termino's restart message."""
        await self.config.restart_message.set(message)
        await ctx.send("Restart message set.")

    @terminoset_restart.command(name="conf")
    async def terminoset_restart_conf(
        self, ctx: commands.Context, *, message: Optional[str] = None
    ) -> None:
        """Set Termino's restart confirmation message."""
        if not message:
            await self.config.restart_confirmation_message.clear()
            return await ctx.send("Restart confirmation disabled.")
        await self.config.restart_confirmation_message.set(message)
        await ctx.send("Restart confirmation message set.")

    @terminoset_shutdown.command(name="message")
    async def terminoset_shutdown_message(self, ctx: commands.Context, *, message: str) -> None:
        """Set Termino's shutdown message."""
        await self.config.shutdown_message.set(message)
        await ctx.send("Shutdown message set.")

    @terminoset_shutdown.command(name="conf")
    async def terminoset_shutdown_conf(
        self, ctx: commands.Context, *, message: Optional[str] = None
    ) -> None:
        """Set Termino's shutdown confirmation message."""
        if not message:
            await self.config.shutdown_confirmation_message.clear()
            return await ctx.send("Shutdown confirmation disabled.")
        await self.config.shutdown_confirmation_message.set(message)
        await ctx.send("Shutdown confirmation message set.")

    @commands.command()
    async def shutdown(self, ctx: commands.Context, force: Optional[bool] = False) -> None:
        """Shuts down the bot.

        Allows [botname] to shut down gracefully.

        This is the recommended method for shutting down the bot.

        Use the `force` argument to skip confirmation (if set).
        """
        if not force:
            force = await self.maybe_confirm(ctx, type="shutdown")
            if not force:
                return
        message = await self.config.shutdown_message()
        await ctx.send(self.format_message(ctx.author, message))
        await self.bot.shutdown()

    @commands.command()
    async def restart(self, ctx: commands.Context, force: Optional[bool] = False) -> None:
        """Attempts to restart [botname].

        Makes [botname] quit with exit code 26.
        The restart is not guaranteed: it must be dealt with by the process manager in use.

        Use the `force` argument to skip confirmation (if set).
        """
        if not force:
            force = await self.maybe_confirm(ctx, type="restart")
            if not force:
                return
        message = await self.config.restart_message()
        await ctx.send(self.format_message(ctx.author, message))
        await self.bot.shutdown(restart=True)

    @terminoset.command(name="settings", aliases=["showsettings"])
    async def terminoset_settings(self, ctx: commands.Context) -> None:
        """Shows the current settings for Termino."""
        config = await self.config.all()
        message_types = (
            "shutdown_message",
            "restart_message",
            "shutdown_confirmation_message",
            "restart_confirmation_message",
        )
        message = ""
        for mt in message_types:
            content = config[mt]
            if not content:
                content = "Not configured (disabled)"
            message += "\n{title}: {content}".format(
                title=mt.replace("_", " ").capitalize(),
                content=content,
            )
        await ctx.send(box(message, lang="yaml"))


def setup(bot: Red) -> None:
    global OLD_SHUTDOWN_COMMAND
    global OLD_RESTART_COMMAND
    OLD_SHUTDOWN_COMMAND = bot.remove_command("shutdown")
    OLD_RESTART_COMMAND = bot.remove_command("restart")
    bot.add_cog(Termino(bot))
