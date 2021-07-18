import asyncio
import contextlib

import discord
from redbot.core import commands
from redbot.core.i18n import Translator
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate

from ...mixins.abc import RaffleMixin
from ...mixins.metaclass import MetaClass
from ...utils.converters import RaffleFactoryConverter

_ = Translator("Raffle", __file__)


class Allowed(RaffleMixin, metaclass=MetaClass):
    """Commands used to edit allowed lists for raffles."""

    @commands.group()
    async def raffle(self, *args, **kwargs):
        pass

    @raffle.group()
    async def edit(self, ctx):
        """Edit the settings for a raffle."""
        pass

    @edit.group()
    async def allowed(self, ctx):
        """Manage the allowed users list in a raffle."""
        pass

    @allowed.command(name="add")
    async def allowed_add(self, ctx, raffle: RaffleFactoryConverter, member: discord.Member):
        """Add a member to the allowed list of a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<member>` - The member to add to the allowed list.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            allowed = raffle_data.get("allowed_users", [])

            if member.id in allowed:
                return await ctx.send(_("This user is already allowed in this raffle."))

            if not allowed:
                raffle_data["allowed_users"] = [member.id]
            else:
                allowed.append(member.id)

            await ctx.send(_("{} added to the allowed list for this raffle.".format(member.name)))

        await self.clean_guild_raffles(ctx)

    @allowed.command(name="remove", aliases=["del"])
    async def allowed_remove(self, ctx, raffle: RaffleFactoryConverter, member: discord.Member):
        """Remove a member from the allowed list of a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<member>` - The member to remove from the allowed list.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            allowed = raffle_data.get("allowed_users", [])

            if member.id not in allowed:
                return await ctx.send(_("This user was not already allowed in this raffle."))

            allowed.remove(member.id)
            if not allowed:
                del raffle_data["allowed_users"]
            await ctx.send(
                _("{} removed from the allowed list for this raffle.".format(member.name))
            )

        await self.clean_guild_raffles(ctx)

    @allowed.command(name="clear")
    async def allowed_clear(self, ctx, raffle: RaffleFactoryConverter):
        """Clear the allowed list for a raffle."""
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            allowed = raffle_data.get("allowed_users", None)

            if allowed is None:
                return await ctx.send(_("There are no allowed users."))

        message = _("Are you sure you want to clear the allowed list for this raffle?")
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

        if predicate.result:
            with contextlib.suppress(KeyError):
                # Still wanna remove empty list here
                del raffle_data["allowed_users"]
            msg = _("Allowed list cleared for this raffle.")
            try:
                await message.edit(content=msg)
            except discord.NotFound:
                await ctx.send(msg)

        else:
            await ctx.send(_("No changes have been made."))

        await self.clean_guild_raffles(ctx)
