import aiohttp

from redbot.core import commands
from redbot.core.utils.chat_formatting import bold


class Quotes(commands.Cog):
    """Get a random quote."""

    __version__ = "1.0.0"
    __author__ = ["Kreusada"]

    def __init__(self, bot):
        self.bot = bot
        self.url = 'https://api.quotable.io/random'
        self.session = aiohttp.ClientSession()

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def formatter(self, content):
        header = bold("From {}")
        return header.format(content["author"]) + f"\n{content['content']}"

    @commands.command()
    async def quote(self, ctx):
        """Get a random quote."""
        async with aiohttp.request("GET", self.url) as r:
            content = await r.json()
        return await ctx.send(self.formatter(content))