import asyncio
import contextlib
import json
from datetime import timedelta
from pathlib import Path
from typing import Literal

import discord
from redbot.core import Config, commands
from redbot.core.bot import Red
from redbot.core.utils.antispam import AntiSpam
from redbot.core.utils.predicates import MessagePredicate

with open(Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]

ANTISPAM_TIMEOUT = 20


class ReplyNoPing(commands.Cog):
    """Sends a message when someone pings you on a reply."""

    __author__ = "Kreusada"
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 48534754387426, True)
        self.config.register_guild(
            message=None,
            toggled=False,
            reply_settings={
                "toggled": True,
                "mention": False,
            },
        )
        self.antispam = {}
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    def cog_unload(self):
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(KeyError):
                self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    @staticmethod
    def determine_reply(message: discord.Message) -> bool:
        message.content = None  # we set this to None to clear message.mentions from actual content
        mentions = message.mentions
        if mentions:  # can only have 1 or 0 elements
            if mentions[0] == message.author or mentions[0].bot:
                return False  # pinged on a reply by the same author, pointless (also bots don't get triggered)
            return True  # pinged on a reply by a different user
        return False  # no mentions == no reply pings, happy days :P
        # it should never get to this last return anyway, seeing as i checked against message.reference in the listener

    @commands.Cog.listener()
    async def on_message_without_command(self, message: discord.Message):
        guild = message.guild
        author = message.author
        channel = message.channel
        if not guild:
            return
        if author.bot:
            return
        if not message.reference:
            return
        channel_perms = channel.permissions_for(guild)
        if not channel_perms.send_messages:
            return
        if await self.bot.cog_disabled_in_guild(self, guild):
            return
        if not await self.bot.ignored_channel_or_guild(message):
            return
        if not await self.bot.allowed_by_whitelist_blacklist(author):
            return
        settings = await self.config.guild(message.guild).all()
        if not settings["toggled"]:
            return
        if not settings["message"]:
            return
        if self.determine_reply(message) is False:
            return
        if guild.id not in self.antispam:
            self.antispam[guild.id] = {}
        if author.id not in self.antispam[guild.id]:
            self.antispam[guild.id][author.id] = AntiSpam(
                [(timedelta(seconds=ANTISPAM_TIMEOUT), 1)]
            )
        if self.antispam[guild.id][author.id].spammy:
            return
        self.antispam[guild.id][author.id].stamp()
        func = self.compose_message(settings, message)
        await func

    @staticmethod
    def compose_message(settings: dict, message: discord.Message):
        kwargs = {"content": settings["message"]}
        reply_settings = settings["reply_settings"]
        if reply_settings["toggled"]:
            func = message.reply
            kwargs["mention_author"] = reply_settings["mention"]
        else:
            func = message.channel.send
        return func(**kwargs)

    @staticmethod
    async def pred(
        ctx: commands.Context, *, message: str, predicate_type: Literal["bool", "input"]
    ):
        await ctx.send(message)
        if predicate_type == "bool":
            pred = MessagePredicate.yes_or_no(ctx, user=ctx.author)
            timeout = 30
        else:
            pred = lambda x: x.author == ctx.author and x.channel == ctx.channel
            timeout = 100
        try:
            message = await ctx.bot.wait_for("message", check=pred, timeout=timeout)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond.")
            return False
        else:
            if predicate_type == "bool":
                return pred.result
            else:
                return message.content

    @commands.group()
    @commands.guild_only()
    @commands.mod_or_permissions(manage_guild=True)
    async def rnp(self, ctx: commands.Context):
        """Configuration for ReplyNoPing."""

    @rnp.command(name="settings")
    async def rnp_settings(self, ctx: commands.Context):
        """View settings for ReplyNoPing for this server."""
        settings = await self.config.guild(ctx.guild).all()
        embed = discord.Embed(
            title="Settings for ReplyNoPing",
            description=f"You can reconfigure all these settings through `{ctx.clean_prefix}rnp set`.",
            colour=await ctx.embed_colour(),
        )
        embed.add_field(name="Enabled:", value=settings["toggled"])
        embed.add_field(name="Replies:", value=settings["reply_settings"]["toggled"])
        embed.add_field(name="Reply mentions:", value=settings["reply_settings"]["mention"])
        embed.add_field(name="Message", value=settings["message"], inline=False)
        embed.set_footer(
            text=f"Triggers will have a {ANTISPAM_TIMEOUT} second timeout per user after each reply ping."
        )
        await ctx.send(embed=embed)

    @rnp.command(name="toggle")
    async def rnp_toggle(self, ctx: commands.Context):
        """Toggle ReplyNoPing for this guild."""
        toggle = await self.config.guild(ctx.guild).toggled()
        new_toggle = not toggle
        await self.config.guild(ctx.guild).toggled.set(new_toggle)
        if new_toggle:
            verb = "enabled"
        else:
            verb = "disabled"
        await ctx.send("ReplyNoPing has been %s for this server." % verb)

    @rnp.command(name="set")
    async def rnp_set(self, ctx: commands.Context):
        """Set up ReplyNoPing for this server."""
        message = await self.pred(
            ctx,
            message="Your next message will be the message sent when users ping on their replies:",
            predicate_type="input",
        )
        reply_toggled = await self.pred(
            ctx,
            message=f"When this message is sent, do you want {self.bot.user.name} to use a reply for their message? (y/n)",
            predicate_type="bool",
        )
        reply_mention = False
        if reply_toggled:
            reply_mention = await self.pred(
                ctx, message="Would you like this reply to mention? (y/n)", predicate_type="bool"
            )
        settings = await self.config.guild(ctx.guild).all()
        toggled = settings["toggled"]
        if toggled is False:
            toggle = await self.pred(
                ctx,
                message=f"ReplyNoPing is currently disabled for this guild. Would you like to enable it now? (y/n)",
                predicate_type="bool",
            )
            settings["toggled"] = toggle
        settings["message"] = message
        settings["reply_settings"]["mention"] = reply_mention
        settings["reply_settings"]["toggled"] = reply_toggled
        await self.config.guild(ctx.guild).set(settings)
        await ctx.send("Settings saved.")


def setup(bot: Red):
    bot.add_cog(ReplyNoPing(bot))
