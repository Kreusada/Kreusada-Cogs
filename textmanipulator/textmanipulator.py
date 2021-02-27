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

import discord

from redbot.core import commands


class TextManipulator(commands.Cog):
    """
    Manipulate characters and text.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.5.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(a for a in self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    @commands.group()
    async def convert(self, ctx: commands.Context):
        """Convert text into different types."""

    @commands.group()
    async def count(self, ctx: commands.Context):
        """Count the number of characters and words."""

    @count.command(aliases=["char"])
    async def characters(self, ctx: commands.Context, *, characters: str):
        """Count how many characters are in a specified text."""
        await ctx.send(
            f"**Including spaces:** {str(len(characters))}\n"
            f"**Excluding spaces:** {str(len(characters) - characters.count(' '))}`"
        )

    @count.command()
    async def words(self, ctx: commands.Context, *, words: str):
        """Count how many words are in a specified text."""
        await ctx.send(f"**Total words:** {str(len(words.split()))}")

    @convert.command()
    async def upper(self, ctx: commands.Context, *, characters: str):
        """Convert all characters to uppercase."""
        await ctx.send(characters.upper())

    @convert.command()
    async def lower(self, ctx: commands.Context, *, characters: str):
        """Convert all characters to lowercase."""
        await ctx.send(characters.lower())

    @convert.command()
    async def title(self, ctx: commands.Context, *, characters: str):
        """Convert all characters to titlecase."""
        await ctx.send(characters.title())

    @convert.command()
    async def snake(self, ctx: commands.Context, *, characters: str):
        """Convert all spaces to underscores."""
        await ctx.send(characters.replace(" ", "_"))

    @convert.command()
    async def alt(self, ctx: commands.Context, *, characters: str):
        """Convert all characters to alternating case."""
        characters = list(characters)
        characters[0::2] = map(str.upper, characters[0::2])
        characters[1::2] = map(str.lower, characters[1::2])
        await ctx.send("".join(characters))

    @commands.command()
    async def remove(self, ctx: commands.Context, char_to_remove: str, *, words: str):
        """Remove characters from text."""
        await ctx.send(list.replace(char_to_remove, ""))

    @commands.command()
    async def escape(self, ctx: commands.Context, *, words: str):
        """Escape markdown."""
        makeraw = discord.utils.escape_markdown(words)
        await ctx.send(makeraw)
