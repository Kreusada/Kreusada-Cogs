from typing import Union

import discord
import names
from redbot.core import commands

full = names.get_full_name
first = names.get_first_name
last = names.get_last_name


class NameGenerator(commands.Cog):
    """
    Generates random names.
    """

    __author__ = ["Kreusada", ]
    __version__ = "2.0.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    @commands.group()
    async def name(self, ctx):
        """Commands for NameGenerator."""

    @name.command(name="full")
    async def _full(self, ctx: commands.Context, gender: str = None):
        """
        Generates a full name.

        Optional arguments:
        `gender`: Provides the gender of the name.
        """
        if gender:
            await ctx.send(full(gender=gender))
        else:
            await ctx.send(full())

    @name.command(name="first")
    async def _first(self, ctx: commands.Context, gender: str = None):
        """
        Generates a first name.

        Optional arguments:
        `gender`: Provides the gender of the name.
        """
        if gender:
            await ctx.send(first(gender=gender))
        else:
            await ctx.send(first())

    @name.command(name="last")
    async def _last(self, ctx: commands.Context):
        """
        Generates a last name.

        Optional arguments:
        `gender`: Provides the gender of the name.
        """
        await ctx.send(last())

    @name.command()
    async def mash(self, ctx, word1: str, word2: str):
        """
        Mash two names together.
        """
        a = word1
        b = word2
        await ctx.send(a[:len(a) // 2].strip() + b[len(b) // 2:].strip())

    @name.command()
    async def mashu(self, ctx, member1: discord.Member, member2: discord.Member, use_nicks: bool = False):
        """
        Mash two usernames together.
        """
        if use_nicks:
            a = member1.display_name
            b = member2.display_name
        else:
            a = member1.name
            b = member2.name
        await ctx.send(a[:len(a) // 2].strip() + b[len(b) // 2:].strip())
