import contextlib
import datetime
import json
import os
import pathlib

from redbot.core import commands

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]

now = lambda: datetime.datetime.utcnow()

header = r"""
______         _           ______ _                       _  ______       _
| ___ \       | |          |  _  (_)                     | | | ___ \     | |
| |_/ /___  __| |  ______  | | | |_ ___  ___ ___  _ __ __| | | |_/ / ___ | |_
|    // _ \/ _` | |______| | | | | / __|/ __/ _ \| '__/ _` | | ___ \/ _ \| __|
| |\ \  __/ (_| |          | |/ /| \__ \ (_| (_) | | | (_| | | |_/ / (_) | |_
\_| \_\___|\__,_|          |___/ |_|___/\___\___/|_|  \__,_| \____/ \___/ \__|
"""

cleared = f"Red console cleared. | {now().strftime('%b %d %Y %H:%M:%S')}."


class ConsoleClearer(commands.Cog):
    """Clear your console."""

    __author__ = "Kreusada"
    __version__ = "1.1.1"

    def __init__(self, bot):
        self.bot = bot
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def cog_unload(self):
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(KeyError):
                self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    @commands.is_owner()
    @commands.command(aliases=["cleanconsole", "consoleclear", "consoleclean"])
    async def clearconsole(self, ctx: commands.Context):
        """
        Completely clears [botname]'s console.
        """
        if os.name == "posix":
            cmd = "clear"
        else:
            cmd = "cls"
        bar = "_" * len(cleared)
        os.system(cmd)
        print(f"{header}\n\n{bar}\n\n{cleared}\n{bar}")
        await ctx.send("Red console cleared.")
