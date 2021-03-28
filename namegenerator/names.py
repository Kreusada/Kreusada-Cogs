"""
MIT License

Copyright (c) 2021 kreusada

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import names
import discord

from redbot.core import commands

full = names.get_full_name
first = names.get_first_name
last = names.get_last_name


class NameGenerator(commands.Cog):
    """
    Generates random names.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.0.0"

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
    async def mash(self, ctx, member1: discord.Member, member2: discord.Member, use_nicks: bool = False):
        """
        Mash two usernames together.
        """
        if use_nicks:
            a = member1.display_name
            b = member2.display_name
        else:
            a = member1.name
            b = member2.name
        await ctx.send(a[:len(a) // 2].strip() + b[len(b) // 2:])
