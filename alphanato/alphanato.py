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

from .alphabet import NATO_ALPHABET


def _remove_whitespace(let):
    return let.replace(' ','')


class AlphaNato(commands.Cog):
    """
    Get the names of the NATO phonetics through easy-to-use syntax.
    """

    __author__ = ["Kreusada"]
    __version__ = "0.3.0"

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

    @commands.command(usage="<letters...>")
    async def nato(self, ctx, *, letter: str):
        """
        Get the nato phonetic name from a letter.

        You may provide multiple letters.
        NOTE: Use `[p]nato all` to get all the NATO phonetics.

        **Example Usage:**
        `[p]nato a, b, c`
        `[p]nato agz`
        `[p]nato z`
        `[p]nato all`

        **Returns:**
        The NATO alphabet name for the provided characters.
        """
        if not letter.isalpha():
            return await ctx.send_help()
        factory = {}
        for x in NATO_ALPHABET:
            if letter.lower().strip() == 'all':
                    factory[x[0].lower()] = x
            else:
                for let in tuple(_remove_whitespace(letter)):
                    if x[0].lower() == let and let.isalpha():
                        factory[let] = x
        msg = "\n".join("'{}' = {}".format(k, v) for k, v in sorted(factory.items()))
        await ctx.send(box(msg, lang='ml'))
