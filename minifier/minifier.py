import contextlib
import io
import json
import pathlib

import discord
import python_minifier as minifier
from redbot.core import commands

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class Minifier(commands.Cog):
    """Minify your code!"""

    __author__ = "Kreusada"
    __version__ = "0.1.3"

    def __init__(self, bot):
        self.bot = bot
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(KeyError):
                self.bot.remove_dev_env_value(self.__class__.__name__.lower())

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
        try:
            file = await file.read()
        except UnicodeDecodeError:
            return await ctx.send("Something went wrong when trying to decode this file.")
        converted = io.BytesIO(minifier.minify(file).encode(encoding="utf-8"))
        return await ctx.send(
            content="Please see the attached file below, with your minified code.",
            file=discord.File(converted, filename=file_name)
        )
