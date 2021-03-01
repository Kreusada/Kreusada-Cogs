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
import logging

from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import bold, box, pagify

log = logging.getLogger("red.kreusada.pingoverride")


class PingOverride(commands.Cog):
    """
    Custom ping message.
    """

    __author__ = ["Kreusada", ]
    __version__ = "1.7.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=59365034743, force_registration=True
        )
        self.config.register_global(
            response="Pong.", reply=False, mention=True, embed=False
        )

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        context = super().format_help_for_context(ctx)
        authors = ", ".join(a for a in self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    def cog_unload(self):
        global _old_ping
        if _old_ping:
            try:
                self.bot.remove_command("ping")
            except Exception as error:
                log.info(error)
            self.bot.add_command(_old_ping)

    async def converter(self, ctx: commands.Context, match, bool):
        if bool:
            mapping = {
                "latency": round(self.bot.latency * 1000),
                "display": ctx.author.display_name,
            }
        else:
            mapping = {
                "latency": f"[latency]",
                "display": "[display_name]",
            }
        return match.format(**mapping)

    @commands.is_owner()
    @commands.group()
    async def pingset(self, ctx: commands.Context):
        """Settings for ping."""

    @pingset.command()
    async def reply(
        self, ctx: commands.Context, true_or_false: bool, mention: bool = False
    ):
        """Set whether ping will use replies in their output."""
        await self.config.reply.set(true_or_false)
        await self.config.mention.set(mention)
        await ctx.tick()
        verb = "now" if true_or_false else "no longer"
        msg = f"Running `{ctx.clean_prefix}ping` will {verb} use replies."
        if not mention:
            if true_or_false:
                msg += " Replies will not mention."
        else:
            msg += " Replies will mention."
        await ctx.send(msg)

    @pingset.command()
    async def settings(self, ctx: commands.Context):
        """Get the settings for the ping command."""
        response = await self.config.response()
        cross = "\N{CROSS MARK}"
        check = "\N{WHITE HEAVY CHECK MARK}"
        if await ctx.embed_requested():
            embed = discord.Embed(
                title=f"Settings for {ctx.bot.user.name}",
                color=await ctx.embed_colour()
            )
            embed.add_field(name="response", value=await self.converter(ctx, response, False), inline=False)
            embed.add_field(name="Replies", value=check if await self.config.reply() else cross, inline=False)
            embed.add_field(name="Reply mentions", value=check if await self.config.mention() else cross, inline=False)
            embed.add_field(name="Embeds", value=check if await self.config.embed() else cross, inline=False)
            await ctx.send(embed=embed)
        else:
            text = (
                f"{bold('Response:')} {await self.converter(ctx, response, False)}\n"
                f"{bold('Replies:')} {await self.config.reply()}\n"
                f"{bold('Reply mentions:')} {await self.config.mention()}\n"
                f"{bold('Use embeds:')} {await self.config.embed()}"
            )
            await ctx.send(text)

    @pingset.command()
    async def embed(self, ctx: commands.Context, true_or_false: bool):
        """
        Toggle whether to use embeds in replies.

        Your message will be put into the description.
        Embeds will not send if they have been disabled via `[p]embedset`.
        """
        await self.config.embed.set(true_or_false)
        verb = "now" if true_or_false else "not"
        await ctx.send(f"`{ctx.clean_prefix}ping` will {verb} use embeds.")

    @pingset.command()
    @commands.guild_only()
    async def message(self, ctx: commands.Context, *, response: str):
        """
        Set your custom ping message.

        Optional Regex:
        `{display}`: Replaces with the authors display name.
        `{latency}`: Replaces with the bots latency.

        Example Usage:
        `[p]pingset message Hello {display}! My latency is {latency} ms.`
        """
        await self.config.response.set(response)
        msg = await self.converter(ctx, response, False)
        embed = await self.config.embed()
        if embed:
            embed = discord.Embed(description=msg, color=await ctx.embed_colour())
            await ctx.send(
                content=f"Running `{ctx.clean_prefix}ping` will now respond with...",
                embed=embed,
            )
        else:
            await ctx.send(
                f"Running `{ctx.clean_prefix}ping` will now respond with... {box(msg, lang='yaml')}"
            )

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Pong. Or not?"""
        resp = await self.config.response()
        reply = await self.config.reply()
        mention = await self.config.mention()
        embed = await self.config.embed()
        message = await self.converter(ctx, resp, True)
        if embed:
            for page in pagify(message, delims=["\n"], page_length=1800):
                embed = discord.Embed(description=page, color=await ctx.embed_colour())
            if reply:
                if await ctx.embed_requested():
                    await ctx.reply(embed=embed, mention_author=mention)
                else:
                    await ctx.reply(message, mention_author=mention)
            else:
                await ctx.maybe_send_embed(message)
        else:
            if reply:
                await ctx.reply(message, mention_author=mention)
            else:
                await ctx.send(message)


def setup(bot):
    cping = PingOverride(bot)
    global _old_ping
    _old_ping = bot.get_command("ping")
    if _old_ping:
        bot.remove_command(_old_ping.name)
    bot.add_cog(cping)
