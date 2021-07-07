import contextlib
import logging

import toml
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

from .enums import PingOverrideVariables
from .objects import Member

log = logging.getLogger("red.kreusada.pingoverride")


def curl(t):
    return "{{{}}}".format(t)


ping_com: commands.Command = None


class PingOverride(commands.Cog):
    """Override the Core's ping command with your own response."""

    settings = {"response": "Pong.", "reply_settings": {"toggled": False, "mention": False}}

    __author__ = ["Kreusada"]
    __version__ = "3.0.0"

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
        kwargs = {"author": Member(ctx.author), "latency": round(self.bot.latency * 1000, 2)}

        sender = ctx.send
        kwargs = {"content": settings["response"].format(**kwargs)}

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
            ping_message.format(
                author=Member(ctx.author), latency=round(self.bot.latency * 1000, 2)
            )
        except KeyError as e:
            curled = curl(str(e).strip("'"))
            await ctx.send(
                box(f"{e.__class__.__name__}: {curled} is not a recognized variable", lang="yaml")
            )
            return
        except commands.BadArgument as e:
            curled = curl(f"author.{e}")
            await ctx.send(
                box(
                    f"{e.__class__.__name__}: {curled} is not valid, author has no attribute {e}",
                    lang="yaml",
                )
            )
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
        await self.config.reply_settings.mention.set(mention)
        verb = "enabled" if mention else "disabled"
        await ctx.send("Reply mentions have been {}.".format(verb))

    @pingset.command(name="variables", aliases=["vars"])
    @commands.bot_has_permissions(add_reactions=True)
    async def pingset_variables(self, ctx: commands.Context):
        """List the available variables for the ping command."""
        data = []
        key = lambda x: x.name
        sorted_vars = sorted(PingOverrideVariables, key=key)
        for c, v in enumerate(sorted_vars, 1):
            if v.name.lower() == "latency":
                var = curl(v.name.lower())
            else:
                var = curl(f"author.{v.name.lower()}")
            _dict = {var: {"description": v.value[1], "example": v.value[2]}}
            page_info = f"Page {c}/{len(sorted_vars)}"
            kwargs = {"text": toml.dumps(_dict) + page_info, "lang": "toml"}
            data.append(box(**kwargs))

        await menu(ctx, data, DEFAULT_CONTROLS)

    @pingset.command(name="settings")
    async def pingset_settings(self, ctx: commands.Context):
        """See the current settings for PingOverride."""
        settings = await self.config.all()
        message = f"Replies: {settings['reply_settings']['toggled']}\n"
        if settings["reply_settings"]["mention"]:
            message += "\t- These replies will mention\n"
        message += f"Response: {settings['response']}"
        await ctx.send(box(message, lang="yaml"))


async def setup(bot):
    global ping_com
    cog = PingOverride(bot)
    ping_com = bot.remove_command("ping")
    await cog.initialize()
    bot.add_cog(cog)
