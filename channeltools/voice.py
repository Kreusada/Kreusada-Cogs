import discord
import lavalink
import datetime

from redbot.core import commands
from redbot.core.utils.chat_formatting import box, italics

from .abc import MixinMeta


class Voice(MixinMeta):
    pass

    @commands.group()
    async def voice(self, ctx):
        """
        Tools for editing voice channels.
        """
        pass

    @voice.command()
    async def lavalogger(self, ctx):
        """Get the socket logger of your lavalink instance."""
        await ctx.send(lavalink.socket_log.name)

    @commands.mod_or_permissions(manage_channels=True)
    @voice.group(name="edit")
    async def voice_edit(self, ctx):
        """Edit a voice channel."""
        pass

    @voice_edit.command()
    async def bitrate(self, ctx, voice_channel: discord.VoiceChannel, bitrate: int):
        """Edit a voice channel's bitrate."""
        if bitrate not in [*range(8000, 96001)]:
            return await ctx.send("Bitrate must be between 8000 and 96000.")
        await voice_channel.edit(bitrate=bitrate)
        await ctx.send(f"Bitrate set to {bitrate}.")

    @voice_edit.command()
    async def name(self, ctx, voice_channel: discord.VoiceChannel, name: str):
        """Edit a voice channel's name."""
        await voice_channel.edit(name=name)
        await ctx.send(f"Name set to {name}.")

    @voice_edit.command()
    async def limit(self, ctx, voice_channel: discord.VoiceChannel, limit: int):
        """Edit a voice channel's user limit."""
        if not limit in [*range(0, 100)]:
            return await ctx.send("User limit must be between 0 and 100.")
        await voice_channel.edit(user_limit=limit)
        if limit == 0:
            return await ctx.send("User limit reset.")
        await ctx.send(f"User limit set to {limit}.")
