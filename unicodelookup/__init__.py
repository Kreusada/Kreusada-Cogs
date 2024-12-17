import unicodedata

import rapidfuzz
from redbot.core import commands
from redbot.core.utils import get_end_user_data_statement
from redbot.core.utils.chat_formatting import inline, pagify
from redbot.core.utils.views import SimpleMenu

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)


class UnicodeLookup(commands.Cog):
    """Search the unicode library for characters and names. Supports fuzzy searching."""

    __author__ = "Kreusada"
    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        return

    @staticmethod
    def fuzzy_lookup(term: str, *, strength: int):
        ret = {}

        # Loop through all Unicode characters
        for codepoint in range(0x110000):
            try:
                name = unicodedata.name(c := chr(codepoint))
                if rapidfuzz.fuzz.ratio(term.lower(), name.lower()) > strength:
                    ret[c] = name
            except ValueError:
                # Ignore characters that don't have a name
                continue

        return ret

    @staticmethod
    async def maybe_send_menu(ctx: commands.Context, *, message: str):
        if len(message) > 500:
            paged = list(pagify(message, page_length=500))
            for i in range(1, len(paged) + 1):
                paged[i - 1] += f"\n\n**(Page {i}/{len(paged)})**"
            menu = SimpleMenu(paged, use_select_menu=True)
            await menu.start(ctx)
        else:
            await ctx.send(message)

    @commands.group(aliases=["unicodelookup"])
    async def ulookup(self, ctx: commands.Context):
        """Unicode lookup commands."""

    @ulookup.command(aliases=["names"])
    async def name(self, ctx: commands.Context, *, characters: str):
        """Get the unicode names of characters."""
        if len(characters) == 1:
            return await ctx.send(f"{inline(characters[0])} - {unicodedata.name(characters[0])}")
        message = "\n".join(
            f"- {inline(c)} - {unicodedata.name(c)}" for c in dict.fromkeys(characters)
        )
        await self.maybe_send_menu(ctx, message=message)

    @ulookup.command()
    async def char(self, ctx: commands.Context, *, name: str):
        """Get the unicode character from the name."""
        try:
            lookup = unicodedata.lookup(name)
        except KeyError:
            await ctx.send(f"No unicode character with the name {name!r} found.")
        else:
            await ctx.send(f"{inline(name.upper())} - {inline(lookup)}")

    @ulookup.command()
    async def fuzzy(
        self, ctx: commands.Context, strength: commands.Range[int, 50, 100] = 80, *, term: str
    ):
        """Get unicode characters from the fuzzy search term.

        Strength must be a number from 50 to 100, used by the fuzzy search algorithm. Defaults to 80 (recommended).
        """
        search = self.fuzzy_lookup(term, strength=strength)
        if not search:
            return await ctx.send("No fuzzy terms found.")
        message = "\n".join(f"- {inline(char)} - {inline(name)}" for char, name in search.items())
        await self.maybe_send_menu(ctx, message=message)


async def setup(bot):
    await bot.add_cog(UnicodeLookup())
