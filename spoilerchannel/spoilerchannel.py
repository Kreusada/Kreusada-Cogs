import contextlib
import logging

import discord
from redbot.core import Config, commands

log = logging.getLogger("red.kreusada.spoilerchannel")


class SpoilerChannel(commands.Cog):
    """Set channels to only have spoilers sent in them."""

    __author__ = ["Kreusada"]
    __version__ = "1.0.1"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 458347565486546, force_registration=True)
        self.config.register_guild(
            channels=[],
        )

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("spoilerchannel")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("spoilerchannel", lambda x: self)

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
        config = await self.config.guild(ctx.guild).channels()
        if channel.id in config:
            return await ctx.send("This channel is already a spoiler channel.")
        await ctx.send("Channel added to the spoiler channel list.")
        config.append(channel.id)
        await self.config.guild(ctx.guild).channels.set(config)

    @spoilerchannel.command()
    async def remove(self, ctx, channel: discord.TextChannel):
        """Remove a channel from the list of spoiler channels."""
        config = await self.config.guild(ctx.guild).channels()
        if not channel.id in config:
            return await ctx.send("This channel is not a spoiler channel.")
        config.remove(channel.id)
        await self.config.guild(ctx.guild).channels.set(config)
        await ctx.send("Channel removed from the spoiler channel list.")

    @spoilerchannel.command(name="list")
    async def _list(self, ctx):
        """List all the spoiler channels."""
        config = await self.config.guild(ctx.guild).channels()
        data = [self.bot.get_channel(x).mention for x in config]
        if ctx.channel.id in config:
            destination = ctx.author
        else:
            destination = ctx
        if not data:
            return await destination.send("There are no channels.")
        await destination.send(", ".join(data))

    @spoilerchannel.command()
    async def clear(self, ctx):
        """Clear the spoiler channel list."""
        await self.config.guild(ctx.guild).channels.clear()
        await ctx.send("Spoiler channel list cleared.")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        config = await self.config.guild(channel.guild).channels()
        if channel.id in config:
            config.remove(channel.id)
            await self.config.guild(channel.guild).channels.set(config)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return
        spoiler_check = lambda x: x.strip().startswith("||") and x.strip().endswith("||")
        channels = await self.config.guild(message.guild).channels()
        if await self.bot.cog_disabled_in_guild(self, message.guild):
            return
        if not await self.bot.ignored_channel_or_guild(message):
            return
        if not message.channel.id in channels:
            return
        if message.attachments:
            for attachment in message.attachments:
                if not attachment.is_spoiler():
                    with contextlib.suppress(discord.Forbidden, discord.NotFound):
                        await message.delete()
                        break
                elif message.content and not spoiler_check(message.content):
                    with contextlib.suppress(discord.Forbidden, discord.NotFound):
                        await message.delete()
                        break
        elif not spoiler_check(message.content):
            with contextlib.suppress(discord.Forbidden, discord.NotFound):
                await message.delete()
