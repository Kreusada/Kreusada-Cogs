import abc
import discord

from redbot.core import commands

from .topic import Topic
from .channel import Channel
from .voice import Voice


class CompositeMetaClass(type(commands.Cog), type(abc.ABC)):
    pass


class ChannelTools(
    Topic,
    Channel,
    Voice,
    commands.Cog,
    metaclass=CompositeMetaClass,
):

    def __init__(self, bot):
        self.bot = bot

    async def embed_builder(self, ctx, title = None, description = None):
        return discord.Embed(
            title=title,
            description=description,
            color=await ctx.embed_colour(),
        )