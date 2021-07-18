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


class RoleRequirements(RaffleMixin, metaclass=MetaClass):
    """Commands used to edit the role requirements lists for raffles."""

    @commands.group()
    async def raffle(self, *args, **kwargs):
        pass

    @raffle.group()
    async def edit(self, ctx):
        """Edit the settings for a raffle."""
        pass

    @edit.group()
    async def rolesreq(self, ctx):
        """Manage role requirements in a raffle."""
        pass

    @rolesreq.command(name="add")
    async def rolesreq_add(self, ctx, raffle: RaffleFactoryConverter, role: discord.Role):
        """Add a role to the role requirements list of a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<role>` - The role to add to the list of role requirements.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            roles = raffle_data.get("roles_needed_to_enter", [])

            if role.id in roles:
                return await ctx.send(_("This role is already a requirement in this raffle."))

            if not roles:
                raffle_data["roles_needed_to_enter"] = [role.id]
            else:
                roles.append(role.id)

            await ctx.send(
                _("{} added to the role requirement list for this raffle.".format(role.name))
            )

        await self.clean_guild_raffles(ctx)

    @rolesreq.command(name="remove", aliases=["del"])
    async def rolereq_remove(self, ctx, raffle: RaffleFactoryConverter, role: discord.Role):
        """Remove a role from the role requirements list of a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<role>` - The role to remove from the list of role requirements.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            roles = raffle_data.get("roles_needed_to_enter", [])

            if role.id not in roles:
                return await ctx.send(_("This role is not already a requirement in this raffle."))

            roles.remove(role.id)
            await ctx.send(
                _("{} remove from the role requirement list for this raffle.".format(role.name))
            )

        await self.clean_guild_raffles(ctx)

    @rolesreq.command(name="clear")
    async def rolereq_clear(self, ctx, raffle: RaffleFactoryConverter):
        """Clear the role requirement list for a raffle.


        **Arguments:**
            - `<raffle>` - The name of the raffle.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            rolesreq = raffle_data.get("roles_needed_to_enter", [])

            if rolesreq is None:
                return await ctx.send(_("There are no required roles."))

            message = _(
                "Are you sure you want to clear the role requirement list for this raffle?"
            )
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
                with contextlib.suppress(KeyError):
                    # Still wanna remove empty list here
                    del raffle_data["roles_needed_to_enter"]
                msg = "Role requirement list cleared for this raffle."
                try:
                    await message.edit(content=msg)
                except discord.NotFound:
                    await ctx.send(msg)

            else:
                await ctx.send(_("No changes have been made."))

            await self.clean_guild_raffles(ctx)
