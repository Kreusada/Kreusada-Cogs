import io
import discord
import python_minifier as minifier

from redbot.core import commands


class Minifier(commands.Cog):
    """Minify your code!"""

    __author__ = ["Kreusada"]
    __version__ = "0.1.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

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
        if not file.filename.lower().endswith(".py"):
            return await ctx.send("Must be a python file.")
        converted = io.BytesIO(minifier.minify(await file.read()).encode())
        content = "Please see the attached file below, with your minimized code."
        await ctx.send(
            content=content,
            file=discord.File(converted, filename=file.filename.lower())
        )
