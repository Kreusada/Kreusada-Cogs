import contextlib
import json
import pathlib

from redbot.core import commands, Config
from redbot.core.commands import Context
from redbot.core.i18n import cog_i18n, Translator
from redbot.core.utils.chat_formatting import humanize_list

from .version_handler import VersionHandler

from .commands.informational import InformationalCommands
from .commands.editor import EditorCommands
from .commands.builder import BuilderCommands

from .commands.management.events import EventCommands
from .commands.management.misc import MiscCommands

from .mixins.metaclass import MetaClass


mixinargs = (InformationalCommands, EditorCommands, BuilderCommands, EventCommands, MiscCommands)

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]

BaseCog = getattr(commands, "Cog", object)
_ = Translator("Raffle", __file__)


@cog_i18n(_)
class Raffle(BaseCog, *mixinargs, metaclass=MetaClass):
    """Create raffles for your server."""

    __author__ = ["Kreusada"]
    __version__ = VersionHandler.versiongetter(True)

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 583475034985340, force_registration=True)
        self.config.register_guild(raffles={})
        self.docs = "https://kreusadacogs.readthedocs.io/en/latest/cog_raffle.html"


    async def replenish_cache(self, ctx: Context) -> None:
        async with self.config.guild(ctx.guild).raffles() as r:

            updates = {}

            for k, v in list(r.items()):

                getter = v.get("owner")
                if not ctx.guild.get_member(getter):
                    del r[k]
                    updates["owner"] = True

                getter = v.get("entries")
                for userid in getter:
                    if not ctx.guild.get_member(userid):
                        getter.remove(userid)
                        updates["entries"] = True

                getter = v.get("prevented_users", None)
                if getter:
                    for userid in getter:
                        if not ctx.guild.get_member(userid):
                            getter.remove(userid)
                            updates["prevented_users"] = True

                getter = v.get("allowed_users", None)
                if getter:
                    for userid in getter:
                        if not ctx.guild.get_member(userid):
                            getter.remove(userid)
                            updates["allowed_users"] = True

                getter = v.get("roles_needed_to_enter", None)
                if getter:
                    for roleid in getter:
                        if not ctx.guild.get_role(roleid):
                            getter.remove(roleid)
                            updates["roles_needed_to_enter"] = True

            return any([updates[x] for x in list(updates.keys())])


    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = humanize_list(self.__author__)
        fmtlink = lambda x, y: f"[{x}]({y})"
        docnote = _(
            "Please consider reading the {docs} if you haven't already.\n\n".format(docs=fmtlink("docs", self.docs))
        )
        return _(
            "{context}\n\n{docnote}Author: {authors}\nVersion: {version}".format(
                context=context,
                docnote=docnote,
                authors=authors,
                version=self.__version__
            )
        )


    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return


    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("raffle")


    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("raffle", lambda x: self)


    async def cog_check(self, ctx: commands.Context):
        return ctx.guild is not None


    @commands.group()
    async def raffle(self, ctx: Context):
        """Manage raffles for your server."""