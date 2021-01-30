import discord
import logging
from redbot.core import Config, commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("PingOverride", __file__)
log = logging.getLogger("red.kreusada.pingoverride")

@cog_i18n(_)
class PingOverride(commands.Cog):
    """
    Custom ping message.
    """

    __author__ = "Kreusada"
    __version__ = "1.4.0"
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=59365034743, force_registration=True)
        self.config.register_global(response="Pong.")

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
    
    @commands.is_owner()  
    @commands.command()
    @commands.guild_only()
    async def pingset(self, ctx: commands.Context, *, response: str):
        """
        Set your custom ping message.
        
        Optional Regex:
        `{display}`: Replaces with the authors display name.
        `{latency}`: Replaces with the bots latency.
        
        Example Usage:
        `[p]pingset Hello {display}! My latency is {latency} ms.`
        """
        await self.config.response.set(response)
        message = await self.converter(ctx, response, False)
        await ctx.send(f"Running `{ctx.clean_prefix}ping` will now respond with:\n{message}")
      
    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Pong. Or not?"""
        resp = await self.config.response()
        message = await self.converter(ctx, resp, True)
        await ctx.send(message)

    
    async def converter(self, ctx: commands.Context, match, bool):
        if bool is True:
            mapping = {"latency": round(self.bot.latency*1000), "display": ctx.author.display_name}
        else:
            mapping = {"latency": f"({ctx.bot.user.name}'s latency)", "display": "(author's display name)"}
        return match.format(**mapping)

async def setup(bot):
    cping = PingOverride(bot)
    global _old_ping
    _old_ping = bot.get_command("ping")
    if _old_ping:
        bot.remove_command(_old_ping.name)
    bot.add_cog(cping)
