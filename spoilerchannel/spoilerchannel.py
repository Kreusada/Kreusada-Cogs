import contextlib
import logging

import discord
from redbot.core import commands, Config

log = logging.getLogger("red.kreusada.spoilerchannel")


class SpoilerChannel(commands.Cog):
    """Set channels to only have spoilers sent in them."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 458347565486546, force_registration=True)
        self.config.register_guild(
            channels=[],
        )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        config = await self.config.guild(channel.guild).channels()
        if channel.id in config:
            config.remove(channel.id)
            await self.config.guild(channel.guild).channels.set(config)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        spoiler_check = lambda x: x.strip().startswith("||") and x.strip().endswith("||")
        channels = await self.config.guild(message.guild).channels()
        if not message.channel.id in channels:
            return
        if message.attachments:
            for attachment in message.attachments:
                if not attachment.is_spoiler():
                    with contextlib.suppress(discord.Forbidden, discord.NotFound):
                        await message.delete()
                elif message.content and not spoiler_check(message.content):
                    with contextlib.suppress(discord.Forbidden, discord.NotFound):
                        await message.delete()
        elif not spoiler_check(message.content):
            with contextlib.suppress(discord.Forbidden, discord.NotFound):
                await message.delete()

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
        config.append(channel.id)
        await self.config.guild(ctx.guild).channels.set(config)
        await ctx.send("Channel added to the spoiler channel list.")

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
        await ctx.send(", ".join(data))

    @spoilerchannel.command()
    async def clear(self, ctx, channel: discord.TextChannel):
        """Clear the spoiler channel list."""
        await self.config.guild(ctx.guild).channels.clear()
        await ctx.send("Spoiler channel list cleared.")