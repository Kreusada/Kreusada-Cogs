import contextlib
import discord
import logging
import time

from redbot.core.bot import Red
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import box

from .enums import PingOverrideVariables
from .objects import Latency, Member

log = logging.getLogger("red.kreusada.pingoverride")


def curl(t):
    return "{{{}}}".format(t)


ping_com: commands.Command = None

class PingOverride(commands.Cog):
    """Override the Core's ping command with your own response."""


    settings = {
        "response": "Pong.",
        "reply_settings": {
            "toggled": False,
            "mention": False
        }
    }


    __author__ = ["Kreusada"]
    __version__ = "2.0.0"


    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 6465983465798475, True)
        self.config.register_global(**self.settings)


    def cog_unload(self):
        global ping_com
        if ping_com:
            try:
                self.bot.remove_command("restart")
            except Exception as e:
                log.info(e)
            self.bot.add_command(ping_com)
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("termino")


    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthors: {authors}\nVersion: {self.__version__}"


    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return


    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("pingoverride", lambda x: self)


    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Pong."""
        settings = await self.config.all()

        sender = ctx.send
        kwargs = {"content": settings["response"].format(author=Member(ctx.author))}

        if settings["reply_settings"]["toggled"]:
            sender = ctx.reply
            kwargs["mention_author"] = settings["reply_settings"]["mention"]

        await sender(**kwargs)


    @commands.group()
    async def pingset(self, ctx: commands.Context):
        """Set your ping message."""

    
    @pingset.command(name="message", aliases=["response"])
    async def pingset_message(self, ctx: commands.Context, *, ping_message: str):
        """Set the ping message sent when a user runs the ping command.
        
        **Variables:**
        
        - `{author.name}`
        - `{author.mention}`
        - `{author.id}`
        - `{author.discriminator}`
        ` `{author.name_and_discriminator}`
        """
        try:
            ping_message.format(author=Member(ctx.author))
        except commands.BadArgument as e:
            curled = curl(f"author.{e}")
            await ctx.send(box(f"{e.__class__.__name__}: {curled} is not valid", lang="yaml"))
            return

        await self.config.response.set(ping_message)
        await ctx.send("The ping response has been set.")


    @pingset.group(name="reply", invoke_without_command=True)
    async def pingset_reply(self, ctx: commands.Context, reply: bool):
        """Set whether the ping message uses replies."""
        await self.config.reply_settings.toggled.set(reply)
        verb = "enabled" if reply else "disabled"
        await ctx.send("Replies have been {}.".format(verb))


    @pingset_reply.command(name="mention")
    async def pingset_reply_mention(self, ctx: commands.Context, mention: bool):
        """Set whether the ping message uses replies."""
        settings = await self.config.all()

        if not settings["reply_settings"]["toggled"]:
            await ctx.send("Replies need to be enabled for this feature.")
            return

        await self.config.reply_settings.mention.set(mention)
        verb = "enabled" if mention else "disabled"
        await ctx.send("Reply mentions have been {}.".format(verb))


    @pingset.command(name="variables", aliases=["vars"])
    async def pingset_variables(self, ctx: commands.Context):
        """List the available variables for the ping command."""
        message = "\n".join(f"{curl('author.' + e.name.lower())}: {e.value[0]}" for e in sorted(PingOverrideVariables, key=lambda x: len(x.name)))
        await ctx.send(box(message, lang="yaml"))


async def setup(bot):
    global ping_com
    cog = PingOverride(bot)
    restart = bot.remove_command("ping")
    await cog.initialize()
    bot.add_cog(cog)