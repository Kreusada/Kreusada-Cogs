import contextlib
import inspect
import json
import pathlib
import random
from typing import Optional

from redbot.core import commands
from redbot.core.utils.chat_formatting import bold, box


class Editor(str):
    """A main class used for the helper functions."""

    def charcount(self, count_spaces: bool) -> str:
        if count_spaces:
            return f"Character count (with spaces): {bold(str(len(self)))}"
        return f"Character count: {bold(len(self) - self.count(' '))}"

    def wordcount(self) -> str:
        return f"Word count: {len(self.split() - self.count(' '))}"

    def occurance(self, check):
        counter = self.count(check)
        plural_check = "once" if counter == 1 else f"{counter} times"
        return f"`{check}` is present in the text {bold(plural_check)}."

    def snake(self) -> str:
        return box(self.replace(" ", "_"))

    def upper(self) -> str:
        return box(super().upper())

    def lower(self) -> str:
        return box(super().lower())

    def title(self) -> str:
        return box(super().title())

    def alternating(self) -> str:
        text = list(self)
        text[0::2] = map(str.upper, text[0::2])
        text[1::2] = map(str.lower, text[1::2])
        return box(text)

    def replace(self, text_to_replace, replacement) -> str:
        replace = lambda x: x.replace(text_to_replace, replacement)
        return box(replace(self))

    def squash(self) -> str:
        return box(self.replace(" ", ""))

    def remove(self, remove) -> str:
        return box(self.replace(remove, ""))

    def trim(self, trimmer) -> str:
        return box(self.strip(trimmer).strip())

    def shuffle(self) -> str:
        data = self.split()
        random.shuffle(data)
        return box(" ".join(data))

    def reverse(self) -> str:
        return box(self[::-1])

    def multiply(self, mul) -> str:
        return box(self * mul)

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class TextEditor(commands.Cog):
    """
    Edit and manipulate with text.
    """

    __author__ = "Kreusada"
    __version__ = "3.0.3"

    def __init__(self, bot):
        self.bot = bot
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    def cog_unload(self):
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(KeyError):
                self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    @commands.group()
    async def editor(self, ctx: commands.Context):
        """Base command for editting text."""

    @editor.command(name="charcount")
    async def editor_charcount(
        self, ctx: commands.Context, include_spaces: Optional[bool] = True, *, text: Editor
    ):
        """Count the number of characters appearing in the text."""
        await ctx.send(text.charcount(include_spaces))

    @editor.command(name="wordcount")
    async def editor_wordcount(self, ctx: commands.Context, *, text: Editor):
        """Count the number of words appearing in the text."""
        await ctx.send(text.wordcount())

    @editor.command(name="occurance")
    async def editor_occurance(self, ctx: commands.Context, check: str, *, text: Editor):
        """Count how many times something appears in the text."""
        await ctx.send(text.occurance(check))

    @editor.command(name="upper")
    async def editor_upper(self, ctx: commands.Context, *, text: Editor):
        """Convert the text to uppercase."""
        await ctx.send(text.upper())

    @editor.command(name="lower")
    async def editor_lower(self, ctx: commands.Context, *, text: Editor):
        """Convert the text to lowercase."""
        await ctx.send(text.lower())

    @editor.command(name="title")
    async def editor_title(self, ctx: commands.Context, *, text: Editor):
        """Convert the text to titlecase."""
        await self.format_text(ctx, inspect.stack()[0][3], text)

    @editor.command(name="snake")
    async def editor_snake(self, ctx: commands.Context, *, text: Editor):
        """Convert all spaces to underscores."""
        await ctx.send(text.snake())

    @editor.command(name="alternating")
    async def editor_alternating(self, ctx: commands.Context, *, text: Editor):
        """Convert the text to alternating case."""
        await ctx.send(text.alternating())

    @editor.command(name="squash")
    async def editor_squash(self, ctx: commands.Context, *, text: Editor):
        """Squash all the words into one."""
        await ctx.send(text.squash())

    @editor.command(name="remove")
    async def editor_remove(self, ctx: commands.Context, remove: str, *, text: Editor):
        """Remove something from the text."""
        await ctx.send(text.remove(remove))

    @editor.command(name="trim", aliases=["strip"], usage='[trimmer=" "] <text>')
    async def editor_trim(self, ctx: commands.Context, trimmer: Optional[str] = " ", *, text: Editor):
        """Trim the outskirts of the text."""
        await ctx.send(text.trim(trimmer))

    @editor.command(name="shuffle", aliases=["jumble"])
    async def editor_shuffle(self, ctx: commands.Context, *, text: Editor):
        """Completely shuffle the text."""
        await ctx.send(text.shuffle())

    @editor.command(name="reverse")
    async def editor_reverse(self, ctx: commands.Context, *, text: Editor):
        """Reverse the text."""
        await ctx.send(text.reverse())

    @editor.command(name="multiply")
    async def editor_multiply(self, ctx: commands.Context, multiplier: int, *, text: Editor):
        """Multiply the text."""
        await ctx.send(text.multiply(multiplier))

    @editor.command(name="replace")
    async def editor_replace(
        self,
        ctx: commands.Context,
        text_to_replace: str,
        replacement: str,
        *,
        text: Editor,
    ):
        """Replace certain parts of the text."""
        await ctx.send(text.replace(text_to_replace, replacement))
