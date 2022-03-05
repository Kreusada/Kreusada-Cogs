import contextlib
import functools
import json
import logging
import pathlib
import random
from datetime import datetime

import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import box

from .objects import Member
from .utils import add_random_messages, curl

log = logging.getLogger("red.kreusada.pingoverride")

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


ping_com: commands.Command = None


class PingOverride(commands.Cog):
    """Override the Core's ping command with your own response."""

    settings = {
        "response": "Pong.",
        "embed": {"toggled": False, "title": "Ping Pong! 🏓"},
        "reply_settings": {"toggled": False, "mention": False},
    }

    __author__ = "Kreusada"
    __version__ = "3.5.4"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 6465983465798475, True)
        self.config.register_global(**self.settings)

        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def cog_unload(self):
        global ping_com
        if ping_com:
            try:
                self.bot.remove_command("ping")
            except Exception as e:
                log.info(e)
            self.bot.add_command(ping_com)
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(KeyError):
                self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

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

        if settings["embed"]["toggled"] and await ctx.embed_requested():
            ekwds = {
                "description": content,
                "color": await ctx.embed_colour(),
                "timestamp": datetime.utcnow(),
            }
            if (title := settings["embed"]["title"]) is not None:
                ekwds["title"] = title.format(**fmt_kwargs)
            embed = discord.Embed(**ekwds)
            kwargs = {"embed": embed}
        else:
            kwargs = {"content": content}

        if settings["reply_settings"]["toggled"]:
            kwargs["mention_author"] = settings["reply_settings"]["mention"]
            kwargs["reference"] = ctx.message.to_reference(fail_if_not_exists=False)

        await ctx.send(**kwargs)

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
        except Exception:
            # catch chained attributeerrors and such
            await ctx.send(
                "This message doesn't look right. Please consult the docs for more information."
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

    @pingset.group(name="embed")
    @commands.bot_has_permissions(embed_links=True)
    async def pingset_embed(self, ctx: commands.Context):
        """Manage the embed settings for the ping command."""

    @pingset_embed.command(name="toggle")
    async def pingset_embed_toggle(self, ctx: commands.Context, toggle: bool):
        """Toggle whether embeds should be enabled for the ping command.

        Note, this will only affect the output if the bot has the permissions to embed.
        """
        await self.config.embed.toggled.set(toggle)
        verb = "enabled" if toggle else "disabled"
        message = "Embeds have been {} for the ping message."
        if toggle:
            message += " You can edit the embed title with `{}pingset embed title`."
        await ctx.send(message.format(verb, ctx.clean_prefix))

    @pingset_embed.command(name="title")
    async def pingset_embed_title(self, ctx: commands.Context, *, title: str = None):
        """Set the title for the embed.

        **Variables:**

        - `{author.name}`
        - `{author.id}`
        - `{author.discriminator}`
        - `{author.name_and_discriminator}`
        - `{latency}`
        """
        if title is not None:
            title = title.replace("{author.mention}", "{author.name}")
            try:
                title.format(author=Member(ctx.author), latency=round(self.bot.latency * 1000, 2))
            except KeyError as e:
                curled = curl(str(e).split("'"))
                await ctx.send(
                    box(
                        f"{e.__class__.__name__}: {curled} is not a recognized variable",
                        lang="yaml",
                    )
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
            except Exception:
                # catch chained attributeerrors and such
                await ctx.send(
                    "This message doesn't look right. Please consult the docs for more information."
                )

            await ctx.send("The embed title has been set.")
        else:
            await ctx.send("Embeds will no longer have a title.")

        await self.config.embed.title.set(title)

    @pingset.command(name="settings")
    async def pingset_settings(self, ctx: commands.Context):
        """See the current settings for PingOverride."""
        settings = await self.config.all()

        message = f"Replies: {settings['reply_settings']['toggled']}\n"
        if settings["reply_settings"]["mention"]:
            message += "\t- These replies will mention\n"
        message += f"Embed:\n\tenabled: {settings['embed']['toggled']}\n\ttitle: {settings['embed']['title']}\n"

        response = settings["response"]
        if isinstance(response, list):
            message += "Responses:\n" + "\n".join(f"\t- {i}" for i in response)
        else:
            message += "Response: " + response
        await ctx.send(box(message, lang="yaml"))


def setup(bot):
    global ping_com
    cog = PingOverride(bot)
    ping_com = bot.remove_command("ping")
    bot.add_cog(cog)
