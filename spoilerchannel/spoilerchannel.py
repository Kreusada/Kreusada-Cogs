import contextlib
import logging
import re

import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import box

log = logging.getLogger("red.kreusada.spoilerchannel")


class SpoilerChannel(commands.Cog):
    """Set channels to only have spoilers sent in them."""

    __author__ = ["Kreusada"]
    __version__ = "2.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 458347565486546, force_registration=True)
        self.config.register_channel(toggled=[])
        self.cache = []
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def cog_unload(self):
        with contextlib.suppress(KeyError):
            self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    async def initialize(self) -> None:
        config = await self.config.all_channels()
        self.cache = list(config.keys())

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    @commands.group()
    async def spoilerchannel(self, ctx):
        """Base command for SpoilerChannel."""
        pass

    @spoilerchannel.command()
    async def add(self, ctx, channel: discord.TextChannel):
        """Add a channel to the list of spoiler channels."""
        if channel.id in self.cache:
            return await ctx.send("This channel is already a spoiler channel.")
        await self.config.channel(channel).toggled.set(True)
        self.cache.append(channel.id)
        await ctx.send("Channel added to the spoiler channel list.")

    @spoilerchannel.command(aliases=["del", "delete"])
    async def remove(self, ctx, channel: discord.TextChannel):
        """Remove a channel from the list of spoiler channels."""
        if channel.id not in self.cache:
            return await ctx.send("This channel is not a spoiler channel.")
        await self.config.channel(channel).toggled.set(False)
        self.cache.remove(channel.id)
        await ctx.send("Channel removed from the spoiler channel list.")

    @spoilerchannel.command(name="list")
    async def _list(self, ctx):
        """List the spoiler channels."""
        channels = box("\n".join(f"+ {ctx.guild.get_channel(c)}" for c in self.cache), lang="diff")
        await ctx.send(f"**Current spoiler-only channels:**\n{channels}")

    @commands.Cog.listener()
    async def on_message_without_command(self, message):
        if message.guild is None:
            return

        channel_perms = message.channel.permissions_for(message.guild)
        if not channel_perms.manage_messages:
            return

        if await self.bot.cog_disabled_in_guild(self, message.guild):
            return

        if not await self.bot.ignored_channel_or_guild(message):
            return

        if not await self.bot.allowed_by_whitelist_blacklist(message.author):
            return

        if not message.channel.id in self.cache:
            return

        if all([message.content, not re.match(r"^\|\|.+\|\|$", message.content)]):
            await message.delete()
            return

        if message.attachments:
            for attachment in message.attachments:
                if not attachment.is_spoiler():
                    await message.delete()

