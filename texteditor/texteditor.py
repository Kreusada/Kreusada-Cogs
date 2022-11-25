import contextlib
import io
import itertools
import json
import pathlib
import random
import shlex
import textwrap
from typing import Optional

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import bold, box, pagify


async def send_safe(ctx, message: str) -> None:
    pages = tuple(pagify(message, page_length=1990))
    if len(pages) > 3:
        raise commands.UserFeedbackCheckFailure(
            "This response contains too many characters. Please be sensible with your inputs."
        )
    for page in pages:
        await ctx.send(box(page))


with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class TextEditor(commands.Cog):
    """
    Edit and manipulate with text.
    """

    __author__ = "Kreusada"
    __version__ = "3.3.0"

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
        """Base command for editing text."""

    @editor.command(name="charcount", aliases=["len"])
    async def editor_charcount(self, ctx: commands.Context, *, text: str):
        """Count the number of characters appearing in the text."""
        await ctx.send(
            f"Character count: **{len(text)}**\n"
            f"Character count (without spaces): **{len(text) - text.count(' ')}**"
        )

    @editor.command(name="wordcount")
    async def editor_wordcount(self, ctx: commands.Context, *, text: str):
        """Count the number of words appearing in the text."""
        await ctx.send(f"Word count: **{len(text.split())}**")

    @editor.command(name="occurance")
    async def editor_occurance(self, ctx: commands.Context, check: str, *, text: str):
        """Count how many times something appears in the text."""
        count = text.count(check)
        plural_check = "once" if count == 1 else f"{count} times"
        await ctx.send(f"`{check}` is present in the text {bold(plural_check)}.")

    @editor.command(name="upper")
    async def editor_upper(self, ctx: commands.Context, *, text: str):
        """Convert the text to uppercase."""
        await send_safe(ctx, text.upper())

    @editor.command(name="lower")
    async def editor_lower(self, ctx: commands.Context, *, text: str):
        """Convert the text to lowercase."""
        await send_safe(ctx, text.lower())

    @editor.command(name="title")
    async def editor_title(self, ctx: commands.Context, *, text: str):
        """Convert the text to titlecase."""
        await send_safe(ctx, text.title())

    @editor.command(name="snake")
    async def editor_snake(self, ctx: commands.Context, *, text: str):
        """Convert all spaces to underscores."""
        await send_safe(ctx, text.replace(" ", "_"))

    @editor.command(name="alternating")
    async def editor_alternating(self, ctx: commands.Context, *, text: str):
        """Convert the text to alternating case."""
        text = list(self)
        text[0::2] = map(str.upper, text[0::2])
        text[1::2] = map(str.lower, text[1::2])
        await send_safe(ctx, "".join(text))

    @editor.command(name="squash")
    async def editor_squash(self, ctx: commands.Context, *, text: str):
        """Squash all the words into one."""
        await send_safe(ctx, text.replace(" ", ""))

    @editor.command(name="remove")
    async def editor_remove(self, ctx: commands.Context, remove: str, *, text: str):
        """Remove something from the text."""
        await send_safe(ctx, text.replace(remove, ""))

    @editor.command(name="trim", aliases=["strip"])
    async def editor_trim(self, ctx: commands.Context, trimmer: Optional[str] = " ", *, text: str):
        """Trim the outskirts of the text."""
        await send_safe(ctx, text.strip(trimmer))

    @editor.command(name="shuffle", aliases=["jumble"])
    async def editor_shuffle(self, ctx: commands.Context, *, text: str):
        """Shuffle the word order in the text."""
        data = text.split()
        random.shuffle(data)
        await send_safe(ctx, " ".join(data))

    @editor.command(name="reverse")
    async def editor_reverse(self, ctx: commands.Context, *, text: str):
        """Reverse the text."""
        await send_safe(ctx, text[::-1])

    @editor.command(name="multiply")
    async def editor_multiply(self, ctx: commands.Context, multiplier: int, *, text: str):
        """Multiply the text."""
        await send_safe(ctx, text * multiplier)

    @editor.command(name="swapcase")
    async def editor_swapcase(self, ctx: commands.Context, *, text: str):
        """Swap the casing for text."""
        await send_safe(ctx, text.swapcase())

    @editor.command(name="camu")
    async def editor_camu(self, ctx: commands.Context, *, text: str):
        """Jumble text in Cambridge University style.

        https://www.mrc-cbu.cam.ac.uk/people/matt.davis/cmabridge/
        """
        ret = []
        for w in text.split():
            tw = list(w)
            if len(w) == 1:
                ret.append(w)
            elif len(w) == 2:
                random.shuffle(tw)
                ret.append(w)
            else:
                mid = tw[1:-1]
                random.shuffle(mid)
                ret.append(w[0] + "".join(mid) + w[-1])
        await send_safe(ctx, " ".join(ret))

    @editor.command(name="permutate", aliases=["permutations"])
    async def editor_permutate(self, ctx: commands.Context, *, text: str):
        """Generate permutations for given combinations of words/digits."""
        if any(map(text.__contains__, "\n`")):
            raise commands.UserFeedbackCheckFailure(
                "Please don't use backticks or newlines in the permutator."
            )
        if len(text) > 250:
            raise commands.UserFeedbackCheckFailure("Too many characters were provided.")
        split = text.split()
        if len(split) > 8:
            raise commands.UserFeedbackCheckFailure("Please only provide up to 8 arguments.")
        permutations = [" ".join(p) for p in itertools.permutations(split)]
        message = "Generated permutations (%s [!%s])" % (len(permutations), len(split))
        join = "\n".join(permutations)
        if len(permutations) > 24:
            message += "\n(See attached file for full permutation)\n\n"
            message += "\n".join(permutations[:24])
            file = discord.File(io.BytesIO(join.encode("utf-8")), filename="permutations.txt")
        else:
            message += "\n" + join
            file = None

        await ctx.send(message=message, file=file)

    @editor.command(name="wrap")
    async def editor_wrap(
        self,
        ctx: commands.Context,
        cut_length: int,
        cut_words: Optional[bool] = True,
        *,
        text: str,
    ):
        """Wrap the text."""
        await send_safe(
            ctx, "\n".join(textwrap.wrap(text, cut_length, break_long_words=cut_words))
        )

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
        await send_safe(ctx, text.replace(text_to_replace, replacement))

    @editor.command(name="shlex")
    async def editor_shlex(self, ctx: commands.Context, *, text: str):
        """Shlex split a given string."""
        await send_safe(ctx, str(shlex.split(text)))

    @editor.command(name="formatnumber", aliases=["commanumber"])
    async def editor_formatnumber(self, ctx: commands.Context, number: int):
        """Format a number with commas."""
        await send_safe(ctx, format(number, ","))

    @editor.command(name="bullet", aliases=["bulletpoint"])
    async def editor_bullet(self, ctx: commands.Context, bullet: str, *items: str):
        """Bullet point a selection of items."""
        await send_safe(ctx, "\n".join(f"{bullet} {item}" for item in items))
