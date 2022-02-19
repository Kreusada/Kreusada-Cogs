import contextlib
import io
import json
import pathlib

import black
import discord
from redbot.core import commands

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class BlackFormatter(commands.Cog):
    """Run black on code."""

    __author__ = "Kreusada"
    __version__ = "1.0.2"

    def __init__(self, bot):
        self.bot = bot
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    def cog_unload(self):
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(KeyError):
                self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    @commands.has_permissions(attach_files=True)
    @commands.command(name="black", usage=f"<file> [line_length={black.DEFAULT_LINE_LENGTH}]")
    async def _black(self, ctx, line_length: int = black.DEFAULT_LINE_LENGTH):
        f"""Format a python file with black.

        You need to attach a file to this command, and it's extension needs to be `.py`.
        Your `line_length` is black setting which defaults to {black.DEFAULT_LINE_LENGTH}.
        """
        await ctx.trigger_typing()
        if not ctx.message.attachments:
            return await ctx.send_help()
        attachment_file = ctx.message.attachments[0]
        if not attachment_file.filename.lower().endswith(".py"):
            return await ctx.send("Must be a python file.")
        file = await attachment_file.read()
        try:
            sort = file.decode(encoding="utf-8")
        except UnicodeDecodeError:
            return await ctx.send("Something went wrong when trying to decode this file.")
        try:
            output = black.format_file_contents(
                sort, fast=True, mode=black.FileMode(line_length=line_length)
            )
        except black.NothingChanged:
            await ctx.send("There was nothing to change in this code.")
        else:
            await ctx.send(
                content="See the attached file below, with your formatted code.",
                file=discord.File(
                    io.BytesIO(output.encode(encoding="utf-8")),
                    filename=attachment_file.filename.lower(),
                ),
            )
