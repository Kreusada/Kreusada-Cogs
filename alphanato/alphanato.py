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

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
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
        factory = {}
        if letter.lower().strip() == 'all':
            for x in NATO_ALPHABET:
                factory[x[0].lower()] = x
            msg = "\n".join("'{}' = {}".format(k, v) for k, v in factory.items())
        else:
            for x in NATO_ALPHABET:
                for let in tuple(_remove_whitespace(letter)):
                    if x[0].lower() == let and x.isalpha():
                        factory[let] = x
                    # X-Ray is weird, so this is required.
                    elif let.lower() == 'x':
                        factory['x'] = NATO_ALPHABET[-3]
            msg = "\n".join("'{}' = {}".format(k, v) for k, v in sorted(factory.items()))
        await ctx.send(box(msg, lang='ml'))