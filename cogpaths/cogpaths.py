import contextlib
import inspect
import json
import os
import pathlib

from redbot.core import commands, data_manager
from redbot.core.config import Config
from redbot.core.utils.chat_formatting import box, humanize_list

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class CogPaths(commands.Cog):
    """Get information about a cog's paths."""

    __author__ = ["Kreusada"]
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = humanize_list(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("cogpaths")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("cogpaths", lambda x: self)

    @commands.command()
    @commands.is_owner()
    async def cogpath(self, ctx: commands.Context, cog: str):
        """Get the paths for a cog."""
        cog_obj = self.bot.get_cog(cog)
        if cog_obj is None:
            await ctx.send("Could not find a cog with this name.")
            return
        cog_path = pathlib.Path(inspect.getfile(cog_obj.__class__)).parent.resolve()
        cog_data_path = pathlib.Path(
            data_manager.cog_data_path() / cog_obj.qualified_name
        ).resolve()
        if not os.path.exists(cog_data_path):
            cog_data_path = None
            if not isinstance(getattr(cog_obj, "config", None), Config):
                reason = "This cog does not store any data."
            else:
                reason = "This cog had its data directory removed."
        message = "Cog path: {}\nData path: {}".format(cog_path, cog_data_path or reason)
        await ctx.send(box(message, lang="yaml"))
