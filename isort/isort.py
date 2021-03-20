import io
import isort
import discord

from redbot.core import commands


class Isort(commands.Cog):
    """Sort imports in your code."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="<file>")
    async def isort(self, ctx):
        if not ctx.message.attachments:
            return await ctx.send_help()
        attachment_file = ctx.message.attachments[0]
        if not attachment_file.filename.lower().endswith(".py"):
            return await ctx.send("Must be a python file.")
        file = await attachment_file.read()
        sort = isort.code(file.decode())
        content = "Please see the attached file below, with your formatted code."
        return await ctx.send(
            content=content,
            file=discord.File(io.BytesIO(sort.encode()), filename=attachment_file.filename.lower())
        )