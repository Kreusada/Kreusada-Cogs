import contextlib
import datetime
import os

from redbot.core import commands

now = datetime.datetime.utcnow()

header = r"""
______         _           ______ _                       _  ______       _
| ___ \       | |          |  _  (_)                     | | | ___ \     | |
| |_/ /___  __| |  ______  | | | |_ ___  ___ ___  _ __ __| | | |_/ / ___ | |_
|    // _ \/ _` | |______| | | | | / __|/ __/ _ \| '__/ _` | | ___ \/ _ \| __|
| |\ \  __/ (_| |          | |/ /| \__ \ (_| (_) | | | (_| | | |_/ / (_) | |_
\_| \_\___|\__,_|          |___/ |_|___/\___\___/|_|  \__,_| \____/ \___/ \__|
"""

cleared = f"Red console cleared. | {now.strftime('%b %d %Y %H:%M:%S')}."


class ConsoleClearer(commands.Cog):
    """Clear your console."""

    __author__ = ["Kreusada"]
    __version__ = "1.1.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("consoleclearer")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("consoleclearer", lambda x: self)

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
