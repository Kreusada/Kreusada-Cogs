import ssl
import aiohttp

from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import bold, warning


class Quotes(commands.Cog):
    """Get a random quote."""

    __version__ = "1.3.0"
    __author__ = "Kreusada"

    def __init__(self, bot: Red):
        self.bot = bot
        self.api = "https://zenquotes.io/api/random"
        self.session = aiohttp.ClientSession()

    async def cog_unload(self):
        await self.session.close()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command()
    async def quote(self, ctx: commands.Context):
        """Get a random quote."""
        await ctx.typing()
        try:
            async with self.session.get(self.api) as r:
                content = await r.json()
        except ssl.SSLCertVerificationError:
            await ctx.send(warning("Unable to connect to the quotes API."))
            return
        await ctx.send(f"From **{content['a']}**\n{content['q']}")
