import discord
import lavalink
import datetime 

from redbot.core import commands
from redbot.core.utils.chat_formatting import box, italics

from .abc import MixinMeta

channel_information = (
    "VC Name: **{0.name}**\nVC ID: **{0.id}**\n"
    "User Limit: **{limit}**\nBitrate: **{0.bitrate}**"
)

user_information = (
    "\n\nMuted: **{0.self_mute}**\nDeafened: **{0.self_deaf}**\n"
    "Streaming: **{0.self_stream}**"
)

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