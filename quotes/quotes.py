import aiohttp

from redbot.core import commands
from redbot.core.utils.chat_formatting import bold


class Quotes(commands.Cog):
    """Get a random quote."""

    def __init__(self, bot):
        self.bot = bot
        self.url = 'https://api.quotable.io/random'
        self.session = aiohttp.ClientSession()

    def formatter(self, content):
        header = bold("From {}")
        return header.format(content["author"]) + f"\n{content['content']}"

    @commands.command()
    async def quote(self, ctx):
        """Get a random quote."""
        async with aiohttp.request("GET", self.url) as r:
            content = await r.json()
        return await ctx.send(self.formatter(content))