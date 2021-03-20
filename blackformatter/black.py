import io
import black
import discord
import contextlib

from redbot.core import commands


class Black(commands.Cog):
    """Run black on code."""

    def __init__(self, bot):
        self.bot = bot

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    @commands.has_permissions(attach_files=True)
    @commands.command(name="black", usage="<file> [line_length=99]")
    async def command(self, ctx, line_length: int = 99):
        """Format a python file with black.

        You need to attach a file to this command, and it's extension needs to be `.py`.
        Your `line_length` is black setting which defaults to 99.
        """
        await ctx.trigger_typing()
        if not ctx.message.attachments:
            return await ctx.send_help()
        attachment_file = ctx.message.attachments[0]
        if not attachment_file.filename.lower().endswith(".py"):
            return await ctx.send("Must be a python file.")
        file = await attachment_file.read()
        sort = file.decode()
        with contextlib.suppress(black.NothingChanged):
            output = black.format_file_contents(sort, fast=True, mode=black.FileMode(line_length=line_length))
            content = "Please see the attached file below, with your formatted code."
            return await ctx.send(
                content=content,
                file=discord.File(io.BytesIO(output.encode()), filename=attachment_file.filename.lower())
            )
        await ctx.send("There was nothing to change in that code.")