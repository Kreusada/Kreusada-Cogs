"""
MIT License

Copyright (c) 2021 kreusada

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord

from redbot.core import commands
from redbot.core.utils.chat_formatting import box


class Codify(commands.Cog):
    """
    Get a message and wrap it in a codeblock.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.0.0"

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
