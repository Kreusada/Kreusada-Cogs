import contextlib
import logging
import random

import discord
import toml
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

from .converters import EmbedTitle
from .enums import PingOverrideVariables
from .objects import Member
from .utils import add_random_messages, curl

log = logging.getLogger("red.kreusada.pingoverride")


ping_com: commands.Command = None


class PingOverride(commands.Cog):
    """Override the Core's ping command with your own response."""

    settings = {
        "response": "Pong.",
        "reply_settings": {"toggled": False, "mention": False},
        "embed": {"toggled": False, "title": None, "color": None},
    }

    __author__ = ["Kreusada"]
    __version__ = "3.3.1"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 6465983465798475, True)
        self.config.register_global(**self.settings)

        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("pingoverride", lambda x: self)

    def cog_unload(self):
        global ping_com
        if ping_com:
            try:
                self.bot.remove_command("ping")
            except Exception as e:
                log.info(e)
            self.bot.add_command(ping_com)
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("pingoverride")

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthors: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Pong."""
        settings = await self.config.all()
        fmt_kwargs = {"author": Member(ctx.author), "latency": round(self.bot.latency * 1000, 2)}

        content = settings["response"]
        if isinstance(content, list):
            content = random.choice(content)
        content = content.format(**fmt_kwargs)

        sender = ctx.send
        kwargs = {}

        if settings["embed"]["toggled"]:
            del settings["embed"]["toggled"]
            if any([v for v in settings["embed"].values()]):
                embed_from_dict = {}
                for k, v in settings["embed"].items():
                    if k == "color" and not v:
                        v = (await ctx.embed_colour()).value
                    if not v:
                        continue
                    embed_from_dict["description"] = content
                    embed_from_dict[k] = v
                kwargs["embed"] = discord.Embed.from_dict(embed_from_dict)
            else:
                kwargs["content"] = content

        else:
            kwargs["content"] = content

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
        - `{author.name_and_discriminator}`
        - `{latency}`
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

        setter = await add_random_messages(ctx, ping_message)

        await self.config.response.set(setter)
        if len(setter) != 1:
            message = "The ping responses have been set."
        else:
            message = "The ping response has been set."
        await ctx.send(message)

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

    @pingset.group(name="embed")
    async def pingset_embed(self, ctx: commands.Context):
        """Manage your ping command's embed."""

    @pingset_embed.command(name="title")
    async def pingset_embed_title(self, ctx: commands.Context, title: EmbedTitle):
        """Set your embed's title."""
        await self.config.embed.title.set(title)
        await ctx.send("Title set.")

    @pingset_embed.command(name="toggle")
    async def pingset_embed_toggle(self, ctx: commands.Context, toggled: bool):
        """Toggle embeds."""
        await self.config.embed.toggled.set(toggled)
        await ctx.send("Embeds are now " + ("on." if toggled else "off."))

    @pingset_embed.command(name="color", aliases=["colour"])
    async def pingset_embed_color(self, ctx: commands.Context, color: discord.Colour = None):
        """Set your embed's color. Leave blank for bot color."""
        if not color:
            message = "Color reset to bot color."
        else:
            message = "Color set to {}".format(str(color))
        await self.config.embed.color.set(color)
        await ctx.send(message)

    @pingset.command(name="settings")
    async def pingset_settings(self, ctx: commands.Context):
        """See the current settings for PingOverride."""
        settings = await self.config.all()

        message = f"Replies: {settings['reply_settings']['toggled']}\n"
        if settings["reply_settings"]["mention"]:
            message += "\t- These replies will mention\n"

        response = settings["response"]
        if isinstance(response, list):
            message += "Responses:\n" + "\n".join(f"\t- {i}" for i in response)
        else:
            message += "Response: " + response
        if settings["embed"]["toggled"]:
            del settings["embed"]["toggled"]
            if any(settings["embed"].values()):
                message += "\nEmbed settings:\n" + "\n".join(
                    f"\t{k}: {v}" for k, v in settings["embed"].items() if v
                )
        else:
            message += "\nEmbed: False"
        await ctx.send(box(message, lang="yaml"))


def setup(bot):
    global ping_com
    cog = PingOverride(bot)
    ping_com = bot.remove_command("ping")
    bot.add_cog(cog)
