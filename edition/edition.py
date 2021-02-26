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

from redbot.core import commands, Config


class Edition(commands.Cog):
    """
    Set your nickname as an edition of someone!
    Inspired by the Twentysix Edition at Red.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.1.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 43958345, force_registration=True)
        self.config.register_guild(editioner=None)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(a for a in self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    @commands.command()
    async def edition(self, ctx: commands.Context, type: str):
        """
        Become an edition of the editioner!

        Server owner nicknames cannot be changed.

        **Arguments**
        `Type`: The custom name from your input.

        **Nickname Edit Format**
        `Editioner - Type Edition`

        **What is Editioner?**
        `Editioner`: The name of the editioner set using `[p]editionset`.
        """
        editioner = await self.config.guild(ctx.guild).editioner()
        editioner = discord.utils.get(ctx.guild.members, id=editioner)
        if editioner is None:
            await ctx.send("You have not setup an editioner yet.")
        else:
            try:
                await ctx.author.edit(
                    nick=f"{editioner.name.capitalize()} - {type} Edition"
                )
                await ctx.send(
                    f"Done. Your nickname is now `{editioner.name.capitalize()} - {type} Edition`."
                )
            except discord.Forbidden:
                await ctx.send(
                    "I don't have permission to change your nickname. Please note that I cannot change server owner nicknames."
                )
            except discord.HTTPException:
                await ctx.send("Your new nickname exceeds the 32 character limit.")

    @commands.command()
    @commands.mod_or_permissions(administrator=True)
    async def editionset(self, ctx: commands.Context, editioner: discord.Member):
        """Sets the editioner."""
        await self.config.guild(ctx.guild).editioner.set(editioner.id)
        await ctx.send(f"Okay, {editioner.name} is now the guild's editioner.")
