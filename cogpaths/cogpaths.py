import inspect
import os
import pathlib

from redbot.core import commands, data_manager
from redbot.core.bot import Red
from redbot.core.commands import CogConverter
from redbot.core.config import Config
from redbot.core.utils.chat_formatting import box


class CogPaths(commands.Cog):
    """Get information about a cog's paths."""

    __author__ = "Kreusada"
    __version__ = "1.2.0"

    def __init__(self, bot: Red):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        return

    @commands.is_owner()
    @commands.command(aliases=["cogpaths"])
    async def cogpath(self, ctx: commands.Context, cog: CogConverter):
        """Get the paths for a cog."""
        cog_path = pathlib.Path(inspect.getfile(cog.__class__)).parent.resolve()
        cog_data_path = pathlib.Path(data_manager.cog_data_path() / cog.qualified_name).resolve()
        if not os.path.exists(cog_data_path):
            cog_data_path = None
            if not isinstance(getattr(cog, "config", None), Config):
                reason = "This cog does not store any data, does not use the `.config` attribute, or does not use Red's Config API."
            else:
                reason = "This cog had its data directory removed."
        message = "Cog path: {}\nData path: {}".format(cog_path, cog_data_path or reason)
        await ctx.send(box(message, lang="yaml"))
