import os
import datetime

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
    __version__ = "1.0.1"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return
        
    @commands.command()
    async def cleanconsole(self, ctx):
        """
        Completely clears [botname]'s console.
        """
        if os.name == 'posix':
            cmd = "clear"
        else:
            cmd = "cls"
        os.system(cmd)
        print(header)
        print()
        print("_" * len(cleared) + '\n')
        print(cleared)
        print("_" * len(cleared))
        await ctx.send("Red console cleared.")