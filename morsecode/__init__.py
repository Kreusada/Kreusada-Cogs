from morse3 import Morse
from redbot.core import commands
from redbot.core.utils import get_end_user_data_statement
from redbot.core.utils.chat_formatting import box, pagify

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)


class MorseCode(commands.Cog):
    """Encode and decode morse code."""

    __author__ = "Kreusada"
    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        return

    @staticmethod
    def safe_morse_encode(text: str):
        try:
            return Morse(text).stringToMorse()
        except Exception as e:
            return str(e)

    @staticmethod
    def safe_morse_decode(morse_code: str):
        try:
            return Morse(morse_code).morseToString()
        except Exception as e:
            return str(e)

    @commands.group()
    async def morse(self, ctx: commands.Context):
        """Encode and decode morse code."""

    @morse.command()
    async def encode(self, ctx: commands.Context, *, text: str):
        """Encode morse code."""
        for page in pagify(self.safe_morse_encode(text), page_length=1990):
            await ctx.send(box(page))

    @morse.command()
    async def decode(self, ctx: commands.Context, *, morse_code: str):
        """Decode morse code."""
        for page in pagify(self.safe_morse_decode(morse_code), page_length=1990):
            await ctx.send(box(page))


async def setup(bot):
    await bot.add_cog(MorseCode())
