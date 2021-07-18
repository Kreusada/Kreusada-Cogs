import asyncio

import discord
from redbot.core import commands
from redbot.core.i18n import Translator
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate

from ...mixins.abc import RaffleMixin
from ...mixins.metaclass import MetaClass
from ...utils.converters import RaffleFactoryConverter

_ = Translator("Raffle", __file__)


class Prevented(RaffleMixin, metaclass=MetaClass):
    """Commands used to edit the prevented lists of raffles."""

    @commands.group()
    async def raffle(self, *args, **kwargs):
        pass

    @raffle.group()
    async def edit(self, ctx):
        """Edit the settings for a raffle."""
        pass

    @edit.group()
    async def prevented(self, ctx):
        """Manage prevented users in a raffle."""
        pass

    @prevented.command(name="add")
    async def prevented_add(self, ctx, raffle: RaffleFactoryConverter, member: discord.Member):
        """Add a member to the prevented list of a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<member>` - The member to add to the prevented list.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            prevented = raffle_data.get("prevented_users", [])

            if member.id in prevented:
                return await ctx.send(_("This user is already prevented in this raffle."))

            if not prevented:
                raffle_data["prevented_users"] = [member.id]
            else:
                prevented.append(member.id)

            await ctx.send(
                _("{} added to the prevented list for this raffle.".format(member.name))
            )

        await self.clean_guild_raffles(ctx)

    @prevented.command(name="remove", aliases=["del"])
    async def prevented_remove(self, ctx, raffle: RaffleFactoryConverter, member: discord.Member):
        """Remove a member from the prevented list of a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<member>` - The member to remove from the prevented list.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            prevented = raffle_data.get("prevented_users", [])

            if member.id not in prevented:
                return await ctx.send(_("This user was not already prevented in this raffle."))

            prevented.remove(member.id)
            if not prevented:
                del raffle_data["prevented_users"]
            await ctx.send(
                _("{} remove from the prevented list for this raffle.".format(member.name))
            )

        await self.clean_guild_raffles(ctx)

    @prevented.command(name="clear")
    async def prevented_clear(self, ctx, raffle: RaffleFactoryConverter):
        """Clear the prevented list for a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            prevented = raffle_data.get("prevented_users", None)

            if prevented is None:
                return await ctx.send(_("There are no prevented users."))

            message = _("Are you sure you want to clear the prevented users list for this raffle?")
            can_react = ctx.channel.permissions_for(ctx.me).add_reactions
            if not can_react:
                message += " (yes/no)"
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
                del raffle_data["prevented_users"]
                msg = _("Prevented users list cleared for this raffle.")
                try:
                    await message.edit(content=msg)
                except discord.NotFound:
                    await ctx.send(msg)

            else:
                await ctx.send(_("No changes have been made."))
