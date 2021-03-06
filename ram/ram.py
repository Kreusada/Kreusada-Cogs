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

import psutil

from redbot.core import commands
from redbot.core.utils.chat_formatting import box

## Thanks Kagami for the .total addon

class RAM(commands.Cog):
    """Get [botname]'s ram."""

    __author__ = ["Kreusada", ]
    __version__ = "1.0.1"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(a for a in self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    @commands.command()
    @commands.is_owner()
    async def ram(self, ctx):
        """Get [botname]'s ram."""
        await ctx.send(
            box(
                text = (
                    f"Percentage: [{psutil.virtual_memory().percent}%]\n"
                    f"Scaled: [{str(round(psutil.virtual_memory().used / 1024 / 1024))}M/"
                    f"{str(round(psutil.virtual_memory().total / 1024 / 1024))}M]"
                ),
                lang="apache"
            )
        )
