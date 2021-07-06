import contextlib
import logging

import aiohttp
from redbot.core import commands
from redbot.core.utils.chat_formatting import bold

log = logging.getLogger("red.kreusada.quotes")


class Quotes(commands.Cog):
    """Get a random quote."""

    __version__ = "1.0.1"
    __author__ = ["Kreusada"]

    def __init__(self, bot):
        self.bot = bot
        self.api = "https://api.quotable.io/random"
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
        log.debug("Session closed.")
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("quotes")

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("quotes", lambda x: self)

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command()
    async def quote(self, ctx):
        """Get a random quote."""
        await ctx.trigger_typing()
        async with self.session.get(self.api) as r:
            content = await r.json()
        formatter = lambda x, y: f"From {bold(x)}\n{y}"
        return await ctx.send(formatter(content["author"], content["content"]))
