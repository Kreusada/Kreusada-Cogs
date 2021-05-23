import contextlib

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box


class Codify(commands.Cog):
    """
    Get a message and wrap it in a codeblock.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.0.1"

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

    @commands.command()
    async def codify(
        self,
        ctx: commands.Context,
        message_id: int,
        language: str = "python",
        escape_markdown: bool = False,
    ):
        """
        Get a message and wrap it in a codeblock.

        Arguments:
        `language`: The language to transform the message content to.
        Defaults to python.
        """
        try:
            message = await ctx.fetch_message(message_id)
            send = box(message.content, lang=language)
            await ctx.send(
                discord.utils.escape_markdown(send)
            ) if escape_markdown else await ctx.send(send)
        except discord.NotFound:
            await ctx.send(f"Could not find a message with the ID: `{message_id}`.")
