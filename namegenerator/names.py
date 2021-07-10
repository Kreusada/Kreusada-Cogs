import contextlib
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

    __author__ = ["Kreusada"]
    __version__ = "2.0.3"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("namegenerator")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("namegenerator", lambda x: self)

    @commands.group()
    async def name(self, ctx):
        """Commands for NameGenerator."""

    @name.command()
    async def full(self, ctx: commands.Context, gender: str = None):
        """
        Generates a full name.

        Optional arguments:
        `gender`: Provides the gender of the name.
        """
        if gender:
            await ctx.send(full(gender=gender))
        else:
            await ctx.send(full())

    @name.command()
    async def first(self, ctx: commands.Context, gender: str = None):
        """
        Generates a first name.

        Optional arguments:
        `gender`: Provides the gender of the name.
        """
        if gender:
            await ctx.send(first(gender=gender))
        else:
            await ctx.send(first())

    @name.command()
    async def last(self, ctx: commands.Context):
        """
        Generates a last name.

        Optional arguments:
        `gender`: Provides the gender of the name.
        """
        await ctx.send(last())

    @name.command()
    async def mash(self, ctx, word1: str, word2: str):
        """
        Mash two words together.
        """
        a = word1
        b = word2
        await ctx.send(a[: len(a) // 2].strip() + b[len(b) // 2 :].strip())
