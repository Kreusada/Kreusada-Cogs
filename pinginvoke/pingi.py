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


class PingInvoke(commands.Cog):
    """
    Bot? [botname]?

    Invoke the ping command by asking if your bot is there.
    """

    __author__ = "Kreusada"
    __version__ = "1.1.1"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 32482347932, force_registration=True)
        self.config.register_global(botname=None)
    
    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        return f"{super().format_help_for_context(ctx)}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    @commands.group()
    @commands.is_owner()
    async def pingi(self, ctx):
        """Commands to configure PingInvoke."""

    @pingi.command(name="set")
    async def _set(self, ctx, botname: str):
        """
        Set the bot name to listen for.

        Example Input:
        `[p]pingi set wall-e`
        `[p]pingi set r2d2`
        `[p]pingi set [botname]`

        Usage:
        When you type [botname]?, or whatever you configure your name as,
        it will invoke the ping command.
        
        NOTE: Do not include the question mark.
        """
        await self.config.botname.set(botname)
        await ctx.send(f"{ctx.me.name} will now invoke the ping command when it hears `{botname}?`.")

    @pingi.command()
    async def reset(self, ctx):
        """Reset and disable PingInvoke."""
        await ctx.tick()
        await self.config.botname.set(None)

    @pingi.command()
    async def settings(self, ctx):
        """Show the current settings for PingInvoke."""
        botname = await self.config.botname()
        if botname:
            await ctx.send(f"{ctx.me.name} will respond to `{botname}?`.")
        else:
            await ctx.send("A name has not been set.")

    @commands.Cog.listener()
    async def on_message_without_command(self, message):
        defa = await self.config.botname()
        if not defa:
            return
        if not message.guild:
            return
        if message.author.bot:
            return
        if message.content.lower().startswith(defa.lower()) and message.content.endswith('?'):
            ctx = await self.bot.get_context(message)
            return await ctx.invoke(self.bot.get_command('ping'))
