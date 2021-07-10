import contextlib
import io

import black
import discord
from redbot.core import commands


class Black(commands.Cog):
    """Run black on code."""

    __author__ = ["Kreusada"]
    __version__ = "0.1.1"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("blackformatter")

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("blackformatter", lambda x: self)

    @commands.has_permissions(attach_files=True)
    @commands.command(name="black", usage="<file> [line_length=99]")
    async def _black(self, ctx, line_length: int = 99):
        """Format a python file with black.

        You need to attach a file to this command, and it's extension needs to be `.py`.
        Your `line_length` is black setting which defaults to 99.
        """
        await ctx.trigger_typing()
        if not ctx.message.attachments:
            return await ctx.send_help()
        attachment_file = ctx.message.attachments[0]
        if not attachment_file.filename.lower().endswith((".py", ".python")):
            return await ctx.send("Must be a python file.")
        file = await attachment_file.read()
        with contextlib.suppress(UnicodeEncodeError, UnicodeDecodeError):
            sort = file.decode(encoding="utf-8")
            with contextlib.suppress(black.NothingChanged):
                output = black.format_file_contents(
                    sort, fast=True, mode=black.FileMode(line_length=line_length)
                )
                content = "Please see the attached file below, with your formatted code."
                return await ctx.send(
                    content=content,
                    file=discord.File(
                        io.BytesIO(output.encode(encoding="utf-8")),
                        filename=attachment_file.filename.lower(),
                    ),
                )
            return await ctx.send("There was nothing to change in that code.")
        return await ctx.send("The file provided was in an unsupported format.")
