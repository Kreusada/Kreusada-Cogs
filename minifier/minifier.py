import contextlib
import io

import discord
import python_minifier as minifier
from redbot.core import commands


class Minifier(commands.Cog):
    """Minify your code!"""

    __author__ = ["Kreusada"]
    __version__ = "0.1.2"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("minifier")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("minifier", lambda x: self)

    @commands.has_permissions(attach_files=True)
    @commands.command(usage="<file>")
    async def minify(self, ctx):
        """Minify a python file.

        You need to attach a file to this command, and it's extension needs to be `.py`.
        """
        await ctx.trigger_typing()
        if not ctx.message.attachments:
            return await ctx.send_help()
        file = ctx.message.attachments[0]
        file_name = file.filename.lower()
        if not file_name.endswith((".py", ".python")):
            return await ctx.send("Must be a python file.")
        with contextlib.suppress(UnicodeDecodeError, UnicodeEncodeError):
            file = await file.read()
            converted = io.BytesIO(minifier.minify(file).encode(encoding="utf-8"))
            content = "Please see the attached file below, with your minimized code."
            return await ctx.send(
                content=content, file=discord.File(converted, filename=file_name)
            )
        return await ctx.send("The file provided was in an unsupported format.")
