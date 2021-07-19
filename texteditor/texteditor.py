import contextlib
import inspect
import random
from typing import Optional

from redbot.core import commands
from redbot.core.utils.chat_formatting import bold, box


class Editor(str):
    """A main class used for the helper functions."""

    def _charcount(self, count_spaces: bool):
        if count_spaces:
            return f"Character count (with spaces): {bold(str(len(self)))}"
        return f"Character count: {bold(len(self) - self.count(' '))}"

    def _wordcount(self):
        return f"Word count: {len(self.split() - self.count(' '))}"

    def _occurance(self, check):
        counter = self.count(check)
        plural_check = "once" if counter == 1 else f"{counter} times"
        return f"`{check}` is present in the text {bold(plural_check)}."

    def _snake(self):
        return box(self.replace(" ", "_"))

    def _alternating(self):
        text = list(self)
        text[0::2] = map(str.upper, text[0::2])
        text[1::2] = map(str.lower, text[1::2])
        return box(text)

    def _replace(self, text_to_replace, replacement):
        replace = lambda x: x.replace(text_to_replace, replacement)
        return box(replace(self))

    def _squash(self):
        return box(self.replace(" ", ""))

    def _remove(self, remove):
        return box(self.replace(remove, ""))

    def _trim(self, trimmer):
        return box(self.strip(trimmer).strip())

    def _shuffle(self):
        data = self.split()
        random.shuffle(data)
        return box(" ".join(data))

    def _reverse(self):
        return box(self[::-1])

    def _multiply(self, mul):
        return box(self * mul)


class TextEditor(commands.Cog):
    """
    Edit and manipulate with text.
    """

    __author__ = ["Kreusada"]
    __version__ = "3.0.1"

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
            self.bot.remove_dev_env_value("texteditor")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("texteditor", lambda x: self)

    async def format_text(self, ctx, function: str, mainbase: str, *args):
        base = Editor(mainbase)
        func = getattr(base, function[6:])
        return await ctx.send(func(*args))

    @commands.group()
    async def editor(self, ctx: commands.Context):
        """Base command for editting text."""

    @editor.command(name="charcount")
    async def editor_charcount(
        self, ctx: commands.Context, include_spaces: Optional[bool] = True, *, text: str
    ):
        """Count the number of characters appearing in the text."""
        await self.format_text(ctx, inspect.stack()[0][3], text, include_spaces)

    @editor.command(name="wordcount")
    async def editor_wordcount(self, ctx: commands.Context, *, text: str):
        """Count the number of words appearing in the text."""
        await self.format_text(ctx, inspect.stack()[0][3], text)

    @editor.command(name="occurance")
    async def editor_occurance(self, ctx: commands.Context, check: str, *, text: str):
        """Count how many times something appears in the text."""
        await self.format_text(ctx, inspect.stack()[0][3], text, check)

    @editor.command(name="upper")
    async def editor_upper(self, ctx: commands.Context, *, text: str):
        """Convert the text to uppercase."""
        await self.format_text(ctx, inspect.stack()[0][3], text)

    @editor.command(name="lower")
    async def editor_lower(self, ctx: commands.Context, *, text: str):
        """Convert the text to lowercase."""
        await self.format_text(ctx, inspect.stack()[0][3], text)

    @editor.command(name="title")
    async def editor_title(self, ctx: commands.Context, *, text: str):
        """Convert the text to titlecase."""
        await self.format_text(ctx, inspect.stack()[0][3], text)

    @editor.command(name="snake")
    async def editor_snake(self, ctx: commands.Context, *, text: str):
        """Convert all spaces to underscores."""
        await self.format_text(ctx, inspect.stack()[0][3], text)

    @editor.command(name="alternating")
    async def editor_alternating(self, ctx: commands.Context, *, text: str):
        """Convert the text to alternating case."""
        await self.format_text(ctx, inspect.stack()[0][3], text)

    @editor.command(name="squash")
    async def editor_squash(self, ctx: commands.Context, *, text: str):
        """Squash all the words into one."""
        await self.format_text(ctx, inspect.stack()[0][3], text)

    @editor.command(name="remove")
    async def editor_remove(self, ctx: commands.Context, remove: str, *, text: str):
        """Remove something from the text."""
        await self.format_text(ctx, inspect.stack()[0][3], text, remove)

    @editor.command(name="trim", aliases=["strip"], usage='[trimmer=" "] <text>')
    async def editor_trim(self, ctx: commands.Context, trimmer: Optional[str] = " ", *, text: str):
        """Trim the outskirts of the text."""
        await self.format_text(ctx, inspect.stack()[0][3], text, trimmer)

    @editor.command(name="shuffle", aliases=["jumble"])
    async def editor_shuffle(self, ctx: commands.Context, *, text: str):
        """Completely shuffle the text."""
        await self.format_text(ctx, inspect.stack()[0][3], text)

    @editor.command(name="reverse")
    async def editor_reverse(self, ctx: commands.Context, *, text: str):
        """Reverse the text."""
        await self.format_text(ctx, inspect.stack()[0][3], text)

    @editor.command(name="multiply")
    async def editor_multiply(self, ctx: commands.Context, multiplier: int, *, text: str):
        """Multiply the text."""
        await self.format_text(ctx, inspect.stack()[0][3], text, multiplier)

    @editor.command(name="replace")
    async def editor_replace(
        self,
        ctx: commands.Context,
        text_to_replace: str,
        replacement: str,
        *,
        text: str,
    ):
        """Replace certain parts of the text."""
        await self.format_text(
            ctx,
            inspect.stack()[0][3],
            text,
            text_to_replace,
            replacement,
        )
