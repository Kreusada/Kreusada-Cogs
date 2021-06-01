import contextlib
from typing import Optional

import discord
import random

from redbot.core import commands
from redbot.core.utils.chat_formatting import bold, box

# TODO: Rewrite


class TextEditor(commands.Cog):
    """
    Edit and manipulate with text.
    """

    __author__ = ["Kreusada"]
    __version__ = "2.0.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("textmanipulator")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("textmanipulator", lambda x: self)

    @commands.group()
    async def editor(self, ctx: commands.Context):
        """Base command for editting text."""

    @editor.command(name="charcount")
    async def editor_charcount(self, ctx: commands.Context, include_spaces: Optional[bool] = True, *, text: str):
        """Count the number of characters appearing in the text."""
        if include_spaces:
            await ctx.send("Character count (with spaces): {}".format(bold(str(len(text)))))
        else:
            await ctx.send("Character count: {}".format(bold(str(len(text) - text.count(" ")))))

    @editor.command(name="wordcount")
    async def editor_wordcount(self, ctx: commands.Context, *, text: str):
        """Count the number of words appearing in the text."""
        count = 0
        for word in text.split():
            if word.isspace():
                continue
            count += 1
        await ctx.send("Word count: {}".format(bold(str(count))))

    @editor.command(name="occurance")
    async def editor_occurance(self, ctx: commands.Context, check: str, *, text: str):
        """Count how many times something appears in the text."""
        counter = text.count(check)
        plural_check = "once" if counter == 1 else f"{counter} times"
        await ctx.send("`{}` is present in the text {}.".format(str(check), bold(plural_check)))

    @editor.command(name="upper")
    async def editor_upper(self, ctx: commands.Context, *, text: str):
        """Convert the text to uppercase."""
        await ctx.send(box(text.upper()))

    @editor.command(name="lower")
    async def editor_lower(self, ctx: commands.Context, *, text: str):
        """Convert the text to lowercase."""
        await ctx.send(box(text.lower()))

    @editor.command(name="title")
    async def editor_title(self, ctx: commands.Context, *, text: str):
        """Convert the text to titlecase."""
        await ctx.send(box(text.title()))

    @editor.command(name="snake")
    async def editor_snake(self, ctx: commands.Context, *, text: str):
        """Convert all spaces to underscores."""
        snake = lambda x: x.replace(" ", "_")
        await ctx.send(box(snake(text)))

    @editor.command(name="alternating")
    async def editor_alternating(self, ctx: commands.Context, *, text: str):
        """Convert the text to alternating case."""
        text = list(text)
        text[0::2] = map(str.upper, text[0::2])
        text[1::2] = map(str.lower, text[1::2])
        await ctx.send(box("".join(text)))

    @editor.command(name="replace")
    async def editor_replace(
        self, 
        ctx: commands.Context, 
        text_to_replace: str,
        replacement: str,
        *, 
        text: str
    ):
        """Replace certain parts of the text."""
        replace = lambda x: x.replace(text_to_replace, replacement)
        await ctx.send(box(replace(text)))

    @editor.command(name="squash")
    async def editor_squash(self, ctx: commands.Context, *, text: str):
        """Squash all the words into one."""
        await ctx.send(box(text.replace(" ", "")))

    @editor.command(name="remove")
    async def editor_remove(self, ctx: commands.Context, remove: str, *, text: str):
        """Remove something from the text."""
        await ctx.send(box(text.replace(remove, "")))

    @editor.command(name="trim", aliases=["strip"])
    async def editor_trim(self, ctx: commands.Context, trimmer: Optional[str] = " ", *, text: str):
        """Trim the outskirts of the text."""
        await ctx.send(box(text.strip(trimmer)))

    @editor.command(name="shuffle", aliases=["jumble"])
    async def editor_shuffle(self, ctx: commands.Context, *, text: str):
        """Completely shuffle the text."""
        data = text.split()
        random.shuffle(data)
        await ctx.send(box(" ".join(data)))

    @editor.command(name="reverse")
    async def editor_reverse(self, ctx: commands.Context, *, text: str):
        """Reverse the text."""
        await ctx.send(box(text[::-1]))