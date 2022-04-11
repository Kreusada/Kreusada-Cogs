import contextlib

from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils import get_end_user_data_statement
from redbot.core.utils.chat_formatting import box, pagify

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)


def safe_chr(digit: int) -> str:
    if digit >= 1114112:
        return "[INVALID]"
    return chr(digit)


class Ordinal(commands.Cog):
    """Get ordinal digits and characters easily."""

    __author__ = "Kreusada"
    __version__ = "1.0.0"

    def __init__(self, bot: Red) -> None:
        self.bot = bot
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    def cog_unload(self) -> None:
        if 719988449867989142 in self.__dev_ids__:
            with contextlib.suppress(KeyError):
                self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    @commands.command(name="ord", usage="[characters...]")
    async def ord_command(self, ctx: commands.Context, *, characters: str) -> None:
        """Get ordinal digits for characters."""
        message = "\n".join(f"ord({c!r}) = {ord(c)}" for c in characters)
        for page in pagify(message, page_length=1990):
            await ctx.send(box(page, lang="py"))

    @commands.command(name="chr", usage="[digits...]")
    async def chr_command(self, ctx: commands.Context, *digits: int) -> None:
        """Get characters from ordinal digits."""
        message = "\n".join(f"chr({d}) = {safe_chr(d)}" for d in digits)
        for page in pagify(message, page_length=1990):
            await ctx.send(box(page, lang="py"))


def setup(bot: Red) -> None:
    bot.add_cog(Ordinal(bot))
