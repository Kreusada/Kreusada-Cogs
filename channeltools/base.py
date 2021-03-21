import abc
import discord
import logging

from redbot.core import commands, Config

from .topic import Topic
from .channel import Channel
from .voice import Voice
from .config import ConfigManager

A = type(commands.Cog)
B = type(abc.ABC)

log = logging.getLogger("red.kreusada.channeltools")


class CompositeMetaClass(A, B):
    pass


class ChannelTools(
    Topic,
    Channel,
    Voice,
    ConfigManager,
    commands.Cog,
    metaclass=ConfigManager,
):
    """A collection of commands used for voice and text channels."""

    __author__ = ["Kreusada"]
    __version__ = "0.0.1"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 658534906834905, force_registration=True)
        self.config.register_guild(topchatters=True)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    async def embed_builder(self, ctx, title = None, description = None):
        return discord.Embed(
            title=title,
            description=description,
            color=await ctx.embed_colour(),
        )

    async def _channel_info_chat_settings(self, ctx):
        config = await self.config.guild(ctx.guild).topchatters()
        return config