import contextlib
import json
import pathlib

from redbot.core import Config, commands
from redbot.core.commands import Context
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import humanize_list

from .commands import Commands
from .mixins.metaclass import MetaClass
from .utils.cleanup import CleanupHelpers
from .version_handler import VersionHandler

RaffleCog = getattr(commands, "Cog", object)
_ = Translator("Raffle", __file__)


with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


mixinargs = (
    CleanupHelpers,
    Commands,
    RaffleCog,
)

version = VersionHandler.__version__


@cog_i18n(_)
class Raffle(*mixinargs, metaclass=MetaClass):
    """Create raffles for your server."""

    __author__ = ["Kreusada"]

    __version__ = VersionHandler.tuple_to_str(version)

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 583475034985340, force_registration=True)
        self.config.register_guild(raffles={})
        self.docs = "https://kreusadacogs.readthedocs.io/en/latest/cog_raffle.html"
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("raffle", lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = humanize_list(self.__author__)
        fmtlink = lambda x, y: f"[{x}]({y})"
        docnote = _(
            "Please consider reading the {docs} if you haven't already.\n\n".format(
                docs=fmtlink("docs", self.docs)
            )
        )
        return _(
            "{context}\n\n{docnote}Author: {authors}\nVersion: {version}".format(
                context=context, docnote=docnote, authors=authors, version=self.__version__
            )
        )

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("raffle")

    async def cog_check(self, ctx: commands.Context):
        return ctx.guild is not None

    @commands.group()
    async def raffle(self, ctx: Context):
        """Manage raffles for your server."""
