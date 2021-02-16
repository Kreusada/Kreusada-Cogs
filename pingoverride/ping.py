import discord
import logging

from redbot.core import Config, commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import bold, box, pagify

_ = Translator("PingOverride", __file__)
log = logging.getLogger("red.kreusada.pingoverride")


@cog_i18n(_)
class PingOverride(commands.Cog):
    """
    Custom ping message.
    """

    __author__ = "Kreusada"
    __version__ = "1.5.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=59365034743, force_registration=True
        )
        self.config.register_global(response="Pong.", reply=False, mention=True, embed=False)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        return f"{super().format_help_for_context(ctx)}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

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
                "latency": f"[{ctx.bot.user.name}'s latency]",
                "display": "[author's display name]",
            }
        return match.format(**mapping)

    @commands.is_owner()
    @commands.group()
    async def pingset(self, ctx):
        """Settings for ping."""

    @pingset.command()
    async def reply(self, ctx, true_or_false: bool, mention: bool = False):
        """Set whether ping will use replies in their output."""
        await self.config.reply.set(true_or_false)
        await self.config.mention.set(mention)
        await ctx.tick()
        verb = "now" if true_or_false else "no longer"
        msg = f"Running `{ctx.clean_prefix}ping` will {verb} use replies."
        if not mention:
            if true_or_false:
                msg = msg + " Replies will not mention."
            else:
                msg = msg
        else:
            msg = msg + " Replies will mention."
        await ctx.send(msg)

    @pingset.command()
    async def settings(self, ctx):
        """Get the settings for the ping command."""
        response = await self.config.response()
        text = (
            f"{bold('Response:')} {box(await self.converter(ctx, response, False), lang='css')}\n"
            f"{bold('Replies:')} {await self.config.reply()}\n"
            f"{bold('Reply mentions:')} {await self.config.mention()}"
        )
        await ctx.send(text)

    @pingset.command()
    async def embed(self, ctx, true_or_false: bool):
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
            await ctx.send(content=f"Running `{ctx.clean_prefix}ping` will now respond with...", embed=embed)
        else:
            await ctx.send(f"Running `{ctx.clean_prefix}ping` will now respond with {box(msg, lang='css')}")

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
                embed = discord.Embed(
                    description=page,
                    color=await ctx.embed_colour()
                )
            if reply:
                if await ctx.embed_requested():
                    await ctx.reply(embed=embed, mention_author=True if mention else False)
                else:
                    await ctx.reply(message, mention_author=True if mention else False)
            else:
                if await ctx.embed_requested():
                    await ctx.send(embed=embed)
                else:
                    await ctx.send(message)
        else:
            if reply:
                await ctx.reply(message, mention_author=True if mention else False)
            else:
                await ctx.send(message)
            
def setup(bot):
    cping = PingOverride(bot)
    global _old_ping
    _old_ping = bot.get_command("ping")
    if _old_ping:
        bot.remove_command(_old_ping.name)
    bot.add_cog(cping)
