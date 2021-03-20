import abc
import discord

from redbot.core import commands

from .topictools import TopicTools
from .channelinfo import ChannelInfo
from .channeleditor import ChannelEditor


class CompositeMetaClass(type(commands.Cog), type(abc.ABC)):
    pass


class ChannelTools(
    TopicTools,
    ChannelInfo,
    ChannelEditor,
    commands.Cog,
    metaclass=CompositeMetaClass,
):

    def __init__(self, bot):
        self.bot = bot

    async def embed_builder(self, ctx, title, description):
        return discord.Embed(
            title=title,
            description=description,
            color=await ctx.embed_colour(),
        )