import contextlib
import logging
from datetime import datetime as dt

import aiohttp
from redbot.core import commands
from redbot.core.utils.chat_formatting import bold

log = logging.getLogger("red.kreusada.githubskyline")


class GithubSkylines(commands.Cog):
    """Get a graph of your contributions on github."""

    __version__ = "1.0.1"
    __author__ = ["Kreusada"]

    def __init__(self, bot):
        self.bot = bot
        self.skyline = "https://skyline.github.com/{}"
        self.session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
        log.debug("Session closed.")
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("githubskylines")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("githubskylines", lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command()
    async def gitskyline(self, ctx, git_username: str, year: int):
        """Get your github skyline for a specified year."""
        await ctx.trigger_typing()
        async with self.session.get(self.skyline.format(git_username)) as session:
            if not session.status == 200:
                return await ctx.send("Please provide a valid github username.")
        if not year in [*range(2008, int(dt.now().strftime("%Y")) + 1)]:
            return await ctx.send(
                f"Please provide a valid year, between 2008 and {dt.now().strftime('%Y')}."
            )
        msg = bold("Here is your github skyline:\n")
        msg += self.skyline.format(git_username) + f"/{year}"
        await ctx.send(msg)
