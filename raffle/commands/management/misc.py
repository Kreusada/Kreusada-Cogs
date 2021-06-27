import asyncio
import contextlib
import discord

from redbot.core import commands
from redbot.core.commands import Context
from redbot.core.i18n import Translator
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate, MessagePredicate

from ...utils.parser import RaffleManager
from ...utils.formatting import tick, cross
from ...mixins.abc import RaffleMixin
from ...utils.exceptions import RaffleError

from ...utils.helpers import (
    validator,
    cleanup_code,
    format_traceback
)

    
_ = Translator("Raffle", __file__)  
    
    
class MiscCommands(RaffleMixin):
    """All the rest of the commands, such as guildowner-only, and ``[p]raffle parse``."""
   

    @commands.group()
    async def raffle(self, ctx: Context):
        pass


    @raffle.command()
    async def parse(self, ctx: Context):
        """Parse a complex raffle without actually creating it."""
        await ctx.trigger_typing()
        check = lambda x: x.author == ctx.author and x.channel == ctx.channel
        message = _(
            "Paste your YAML here. It will be validated, and if there is "
            "an exception, it will be returned to you."

        )

        await ctx.send(message)  

        try:
            content = await self.bot.wait_for("message", timeout=500, check=check)
        except asyncio.TimeoutError:
            with contextlib.suppress(discord.NotFound):
                await message.delete()


        content = content.content
        valid = validator(cleanup_code(content))

        if not valid:
            return await ctx.send(_("This YAML is invalid."))

        try:
            parser = RaffleManager(valid)
            parser.parser(ctx)
        except RaffleError as e:
            exc = _("An exception occured whilst parsing your data.")
            return await ctx.send(cross(exc) + format_traceback(e))
        
        await ctx.send(tick(_("This YAML is good to go! No errors were found.")))

        await self.replenish_cache(ctx)
    

    @raffle.command()
    @commands.guildowner()
    async def refresh(self, ctx: Context):
        """Refresh all of the raffle caches."""
        cleaner = await self.replenish_cache(ctx)
        if cleaner:
            return await ctx.send(_("Raffles updated."))
        else:
            return await ctx.send(_("Everything was already up to date."))


    @raffle.command()
    @commands.guildowner()
    async def teardown(self, ctx: Context):
        """End ALL ongoing raffles."""
        raffles = await self.config.guild(ctx.guild).raffles()

        if not raffles:
            await ctx.send(_("There are no ongoing raffles in this guild."))
            return

        message = _("Are you sure you want to tear down all ongoing raffles in this guild?")
        can_react = ctx.channel.permissions_for(ctx.me).add_reactions
        if not can_react:
            message += " (y/n)"
        message = await ctx.send(message)
        if can_react:
            start_adding_reactions(message, ReactionPredicate.YES_OR_NO_EMOJIS)
            predicate = ReactionPredicate.yes_or_no(message, ctx.author)
            event_type = "reaction_add"
        else:
            predicate = MessagePredicate.yes_or_no(ctx)
            event_type = "message"
        
        try:
            await self.bot.wait_for(event_type, check=predicate, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send(_("You took too long to respond."))
            return

        with contextlib.suppress(discord.NotFound):
            await message.delete()

        if predicate.result:
            async with self.config.guild(ctx.guild).raffles() as r:
                r.clear()
            await ctx.send(_("Raffles cleared."))
        
        else:
            await ctx.send(_("No changes have been made."))

        await self.replenish_cache(ctx)
