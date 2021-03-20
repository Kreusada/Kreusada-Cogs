import io
import isort
import black
import discord
import python_minifier as minifier

from redbot.core import commands
from redbot.core.utils.predicates import MessagePredicate


class Minifier(commands.Cog):
    """Minify your code!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="<file>")
    async def minify(self, ctx):
        if not ctx.message.attachments:
            return await ctx.send_help()
        file = ctx.message.attachments[0]
        if not file.filename.lower().endswith(".py"):
            return await ctx.send("Must be a python file.")
        converted = io.BytesIO(minifier.minify(await file.read()).encode())
        content = "Please see the attached file below, with your minimized code."
        await ctx.send(
            content=content,
            file=discord.File(converted, filename=file.filename.lower())
        )