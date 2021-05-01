import discord

from redbot.core import commands

from .builder import Builder
from .exceptions import (
    ParserError,
    ParserHexError,
    ParserURLError,
    ParserInvalidItemError,
    ParserInvalidTypeError
)
from .functions import (
    yaml_parser,
    cleanup_code
)
from .mixins import MixinMeta
from .parser import Parser

class Commands(MixinMeta):
    """
    Seperate file for all the interactable commands
    within the cog.

    The functions also trigger the parser and builder
    classes.

    Settings and config is found in settings.py
    """

    @commands.group()
    async def embed(self, ctx):
        """Create, manage, and store embeds."""

    @embed.command(name="create")
    async def embed_create(self, ctx):
        """Create an embed using YAML."""
        check = lambda x: x.author == ctx.author and x.channel == ctx.channel
        await ctx.send(
            "Now you need to compose your YAML. For reference, see below: "
            + example_cog_creation_yaml
        )
        try:
            content = await self.bot.wait_for("message", timeout=250, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long to respond.")
        content = content.content
        async with ctx.typing():
            await yaml_parser(ctx, content, "creation")
