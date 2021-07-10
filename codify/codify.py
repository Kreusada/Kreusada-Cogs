import contextlib

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box


def cleanup_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:-1])
    return content.strip("` \n")


class Codify(commands.Cog):
    """
    Place text inside of codeblocks.
    """

    __author__ = ["Kreusada"]
    __version__ = "2.0.0"

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
            self.bot.remove_dev_env_value("codify")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("codify", lambda x: self)

    @commands.group()
    async def codify(self, ctx: commands.Context):
        """Wrap text in codeblocks."""

    @codify.command(usage="<message id> <codeblock language>")
    async def frommsg(self, ctx: commands.Context, message_id: int, language: str = "python"):
        """Get a message and wrap it in a codeblock."""
        try:
            message = await ctx.fetch_message(message_id)
            content = cleanup_code(message.content)
            send = await ctx.send(box(content, lang=language))
            await ctx.tick()
        except discord.NotFound:
            await ctx.send("Could not find a message with that ID.")

    @codify.command(aliases=["fromstr"], usage="<codeblock language> <text>")
    async def fromtext(self, ctx: commands.Context, language: str = "python", *, text: str):
        """Wrap custom text into a codeblock."""
        await ctx.send(box(text, lang=language))
        await ctx.tick()
