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

import contextlib
import discord
import logging
import asyncio
import random

from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import bold, box, pagify
from redbot.core.utils.predicates import ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions

log = logging.getLogger("red.kreusada.pingoverride")


class PingOverride(commands.Cog):
    """
    Custom ping message.
    """

    __author__ = [
        "Kreusada",
    ]
    __version__ = "1.8.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=59365034743, force_registration=True
        )
        self.config.register_global(response=[], reply=False, mention=True, embed=False)

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
                "latency": "[latency]",
                "display": "[display_name]",
            }
        with contextlib.suppress(KeyError):
            # Cannot return on exception here
            return match.format(**mapping)

    async def enum(self, ctx, message_list):
        msg_list = [await self.converter(ctx, x, False) for x in message_list]
        try:
            pre_processed = box(
                "\n".join(f"+ {c+1}: {self.shorten(v)}" for c, v in enumerate(msg_list)),
                lang="diff",
            )
            message = f"The following responses have been set! {pre_processed}"

            response = await self.config.response()
            for z in message_list:
                response.append(z)
            await self.config.response.set(response)

            return await ctx.send(message)
        except TypeError:
            return await ctx.send("Something went wrong when compiling your regex. Your responses have been reset.")

    @staticmethod
    def shorten(text):
        if len(text) > 30:
            return text[:30] + "..."
        else:
            return text

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
        cross = "\N{CROSS MARK}"
        check = "\N{WHITE HEAVY CHECK MARK}"

        response = await self.config.response()
        reply = await self.config.reply()
        mention = await self.config.mention()
        embed = await self.config.embed()

        if not response:
            pre_processed = "+ Pong."
        else:
            message_list = [await self.converter(ctx, x, False) for x in response]
            pre_processed = "\n".join(
                f"+ {c+1}: {self.shorten(v)}" for c, v in enumerate(message_list)
            )

        pre_processed = box(pre_processed, lang="diff")

        if await ctx.embed_requested():
            output = discord.Embed(
                title=f"Ping Settings for {ctx.bot.user.name}",
                color=await ctx.embed_colour(),
            )

            output.add_field(
                name="Replies", value=check if reply else cross, inline=True
            )

            if reply:
                output.add_field(
                    name="Reply mentions",
                    value=check if mention else cross,
                    inline=True,
                )

            output.add_field(name="Embeds", value=check if embed else cross, inline=True)
            output.add_field(name="Responses", value=pre_processed, inline=False)
            output.set_footer(text=f"See {ctx.clean_prefix}pingset regex, for information on response regex.")

            await ctx.send(embed=output)
        else:
            await ctx.send("I need to be able to send embeds.")

    @pingset.command()
    async def regex(self, ctx: commands.Context):
        """Get information on the types of ping regex."""
        description = "`{latency}`: Bot Latency\n`{display}`: Author's Display Name"
        if await ctx.embed_requested():
            await ctx.send(
                embed=discord.Embed(
                    description=description, color=await ctx.embed_colour()
                )
            )
        else:
            await ctx.send(description)

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
    async def message(self, ctx: commands.Context, *, message: str):
        """
        Set your custom ping message.

        Optional Regex:
        `{display}`: Replaces with the authors display name.
        `{latency}`: Replaces with the bots latency.

        Example Usage:
        `[p]pingset message Hello {display}! My latency is {latency} ms.`
        """

        msg = await ctx.send(
            "Would you like to add any other responses, to be chosen at random?"
        )
        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        try:
            await self.bot.wait_for("reaction_add", check=pred, timeout=30)
        except asyncio.TimeoutError:
            await self.config.response.clear()
            response = await self.config.response()
            response.append(message)
            await self.config.response.set(response)
            return await ctx.send(
                "You took too long to answer, I'll stick to this one response!"
            )

        if pred.result:
            await ctx.send("Okay, let's add some random responses.")
            await self.config.response.clear()

            message_list = [message]
            response = await self.config.response()

            while True:

                if len(message_list) > 9:
                    await ctx.send("You've reached the maximum number of responses!")
                    return await self.enum(ctx, message_list)

                await ctx.send("Add a random response:")

                def check(x):
                    return x.author == ctx.author and x.channel == ctx.channel

                try:
                    add_response = await self.bot.wait_for(
                        "message", timeout=50, check=check
                    )
                except asyncio.TimeoutError:
                    return await ctx.send("Timed out. No changes have been made.")

                if add_response.content.lower().startswith(("exit()", "stop()")):
                    await ctx.send("Ended!")
                    return await self.enum(ctx, message_list)
                else:
                    message_list.append(add_response.content)

        else:
            await self.config.response.clear()
            response = await self.config.response()
            response.append(message)
            await self.config.response.set(response)
            return await ctx.send("Ok, I'll stick to this one response!")

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Pong. Or not?"""
        resp = await self.config.response()
        if not resp:
            resp = "Pong."
        else:
            resp = random.choice(resp)
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