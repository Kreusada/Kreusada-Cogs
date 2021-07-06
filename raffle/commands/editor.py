import asyncio
import contextlib
from typing import Union

import discord
from redbot.core import commands
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import box, inline
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate

from ..mixins.abc import RaffleMixin
from ..utils.checks import VALID_USER_BADGES
from ..utils.converters import RaffleFactoryConverter
from ..utils.exceptions import InvalidArgument, RaffleError
from ..utils.formatting import cross, tick
from ..utils.helpers import (
    cleanup_code,
    format_traceback,
    format_underscored_text,
    raffle_safe_member_scanner,
    start_interactive_message_session,
    validator,
)
from ..utils.parser import RaffleManager

_ = Translator("Raffle", __file__)


class EditorCommands(RaffleMixin):
    """Mixin for commands under ``[p]raffle edit``."""

    @commands.group()
    async def raffle(self, ctx):
        pass

    @raffle.group()
    async def edit(self, ctx):
        """Edit the settings for a raffle."""
        pass

    @edit.command()
    async def accage(self, ctx, raffle: RaffleFactoryConverter, new_account_age: Union[int, bool]):
        """Edit the account age requirement for a raffle.

        Use `0` or `false` to disable this condition.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<new_account_age>` - The new account age requirement.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            if isinstance(new_account_age, bool):
                if not new_account_age:
                    with contextlib.suppress(KeyError):
                        del raffle_data["account_age"]
                    return await ctx.send(_("Account age requirement removed from this raffle."))
                else:
                    return await ctx.send(
                        _('Please provide a number, or "false" to disable this condition.')
                    )

            try:
                RaffleManager.parse_accage(new_account_age)
            except InvalidArgument as e:
                return await ctx.send(format_traceback(e))

            raffle_data["account_age"] = new_account_age
            await ctx.send(_("Account age requirement updated for this raffle."))

        await self.replenish_cache(ctx)

    @edit.command()
    async def serverjoinage(
        self, ctx, raffle: RaffleFactoryConverter, new_server_join_age: Union[int, bool]
    ):
        """Edit the server join age requirement for a raffle.

        Use `0` or `false` to disable this condition.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<new_server_join_age>` - The new join age requirement.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            if not new_server_join_age:
                with contextlib.suppress(KeyError):
                    del raffle_data["server_join_age"]
                return await ctx.send(_("Server join age requirement removed from this raffle."))

            elif new_server_join_age is True:
                return await ctx.send(
                    _('Please provide a number, or "false" to disable this condition.')
                )

            else:
                try:
                    RaffleManager.parse_serverjoinage(ctx, new_server_join_age)
                except InvalidArgument as e:
                    return await ctx.send(format_traceback(e))

                raffle_data["server_join_age"] = new_server_join_age
                await ctx.send(_("Server join age requirement updated for this raffle."))

        await self.replenish_cache(ctx)

    @edit.command()
    async def description(
        self, ctx, raffle: RaffleFactoryConverter, *, description: Union[bool, str]
    ):
        """Edit the description for a raffle.

        Use `0` or `false` to remove this feature.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<description>` - The new description.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            if not description:
                with contextlib.suppress(KeyError):
                    del raffle_data["description"]
                return await ctx.send(_("Description removed from this raffle."))

            elif description is True:
                return await ctx.send(
                    _('Please provide a number, or "false" to disable the description.')
                )

            else:
                raffle_data["description"] = description
                await ctx.send(_("Description updated for this raffle."))

        await self.replenish_cache(ctx)

    @edit.command()
    async def endaction(
        self, ctx, raffle: RaffleFactoryConverter, *, on_end_action: Union[bool, str]
    ):
        """Edit the on_end_action for a raffle.

        Use `0` or `false` to remove this feature.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<on_end_action>` - The new action. Must be one of `end`, `remove_winner`, 'remove_and_prevent_winner', or `keep_winner`.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            if not on_end_action:
                with contextlib.suppress(KeyError):
                    del raffle_data["on_end_action"]
                return await ctx.send(_("On end action reset to the default: `keep_winner`."))

            elif on_end_action is True:
                return await ctx.send(
                    _('Please provide a number, or "false" to disable the description.')
                )

            else:
                if not on_end_action in (
                    "end",
                    "remove_winner",
                    "remove_and_prevent_winner",
                    "keep_winner",
                ):
                    return await ctx.send(
                        _(
                            "Please provide one of `end`, `remove_winner`, `remove_and_prevent_winner`, or `keep_winner`."
                        )
                    )
                raffle_data["on_end_action"] = on_end_action
                await ctx.send(_("On end action updated for this raffle."))

        await self.replenish_cache(ctx)

    @edit.command()
    async def maxentries(
        self, ctx, raffle: RaffleFactoryConverter, maximum_entries: Union[int, bool]
    ):
        """Edit the max entries requirement for a raffle.

        Use `0` or `false` to disable this condition.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<maximum_entries>` - The new maximum number of entries.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            if not maximum_entries:
                with contextlib.suppress(KeyError):
                    del raffle_data["maximum_entries"]
                return await ctx.send(_("Maximum entries condition removed from this raffle."))

            elif maximum_entries is True:
                return await ctx.send(
                    _('Please provide a number, or "false" to disable this condition.')
                )

            else:
                raffle_data["maximum_entries"] = maximum_entries
                await ctx.send(_("Max entries requirement updated for this raffle."))

        await self.replenish_cache(ctx)

    @edit.command()
    async def endmessage(
        self, ctx, raffle: RaffleFactoryConverter, *, end_message: Union[bool, str]
    ):
        """Edit the end message of a raffle.

        Once you provide an end message, you will have the chance
        to add additional messages, which will be selected at random
        when a winner is drawn.

        Use `0` or `false` to disable this condition.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<end_message>` - The new ending message.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            if not end_message:
                with contextlib.suppress(KeyError):
                    del raffle_data["end_message"]
                return await ctx.send(
                    _("End message feature removed from this raffle. It will now use the default.")
                )

            elif end_message is True:
                return await ctx.send(
                    _('Please provide a number, or "false" to disable this condition.')
                )

            else:
                try:
                    raffle_safe_member_scanner(end_message, "end_message")
                except InvalidArgument as e:
                    return await ctx.send(format_traceback(e))

                message = _(
                    "Would you like to add additional end messages to be selected from at random?"
                )

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
                    await ctx.send(
                        _(
                            'You took too long to respond. Saving end message as "{}".'.format(
                                end_message
                            )
                        )
                    )

                if predicate.result:
                    interaction = await start_interactive_message_session(
                        ctx, self.bot, "end_message", message
                    )
                    if interaction is False:
                        data = end_message
                        await ctx.send(
                            _(
                                "End message set to what you provided previously: {}".format(
                                    end_message
                                )
                            )
                        )
                    else:
                        data = [end_message] + interaction
                        await ctx.send(_("End messages updated for this raffle."))
                else:
                    data = end_message
                    await ctx.send(_("End message updated for this raffle."))
                raffle_data["end_message"] = data

        await self.replenish_cache(ctx)

    @edit.command()
    async def joinmessage(
        self, ctx, raffle: RaffleFactoryConverter, *, join_message: Union[bool, str]
    ):
        """Edit the join message of a raffle.

        Once you provide a join message, you will have the chance
        to add additional messages, which will be selected at random
        when a user joins the raffle.

        Use `0` or `false` to disable this condition.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<join_message>` - The new joining message.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            if not join_message:
                with contextlib.suppress(KeyError):
                    del raffle_data["join_message"]
                return await ctx.send(
                    _(
                        "Join message feature removed from this raffle. It will now use the default."
                    )
                )

            elif join_message is True:
                return await ctx.send(
                    _('Please provide a number, or "false" to disable this condition.')
                )

            else:
                try:
                    raffle_safe_member_scanner(join_message, "join_message")
                except InvalidArgument as e:
                    return await ctx.send(format_traceback(e))

                message = _(
                    "Would you like to add additional end messages to be selected from at random?"
                )

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
                    await ctx.send(
                        _(
                            'You took too long to respond. Saving join message as "{}".'.format(
                                join_message
                            )
                        )
                    )

                if predicate.result:
                    interaction = await start_interactive_message_session(
                        ctx, self.bot, "join_message", message
                    )
                    if interaction is False:
                        data = join_message
                        await ctx.send(
                            _(
                                "Join message set to what you provided previously: {}".format(
                                    join_message
                                )
                            )
                        )
                    else:
                        data = [join_message] + interaction
                        await ctx.send(_("Join messages updated for this raffle."))
                else:
                    data = join_message
                    await ctx.send(_("Join message updated for this raffle."))
                raffle_data["join_message"] = data

        await self.replenish_cache(ctx)

    @edit.command()
    async def fromyaml(self, ctx, raffle: RaffleFactoryConverter):
        """Edit a raffle directly from yaml.

        **Arguments:**
            - `<raffle>` - The name of the raffle to edit.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

        existing_data = {
            "end_message": raffle_data.get("end_message", None),
            "join_message": raffle_data.get("join_message", None),
            "account_age": raffle_data.get("account_age", None),
            "server_join_age": raffle_data.get("server_join_age", None),
            "roles_needed_to_enter": raffle_data.get("roles_needed_to_enter", None),
            "badges_needed_to_enter": raffle_data.get("badges_needed_to_enter", None),
            "prevented_users": raffle_data.get("prevented_users", None),
            "allowed_users": raffle_data.get("allowed_users", None),
            "description": raffle_data.get("description", None),
            "maximum_entries": raffle_data.get("maximum_entries", None),
            "on_end_action": raffle_data.get("on_end_action", None),
        }

        message = (
            _(
                "You're about to **edit an existing raffle**.\n\nThe `name` "
                "block cannot be edited through this command, it's preferred "
                "if you create a new raffle with the new name instead.\nYou can end "
                "this raffle through using `{prefix}raffle end {raffle}`."
                "\nPlease consider reading the docs about the various "
                "conditional blocks if you haven't already.\n\n".format(
                    prefix=ctx.clean_prefix, raffle=raffle
                )
            )
            + self.docs
        )

        quotes = lambda x: f'"{x}"'
        noedits = lambda x: _("{x} # Cannot be edited".format(x=x))
        relevant_data = [("name", noedits(quotes(raffle)))]
        for k, v in raffle_data.items():
            if k in ("owner", "entries", "created_at"):
                # These are not user defined keys
                continue
            if isinstance(v, str):
                v = quotes(v)
            relevant_data.append((k, v))

        message += _(
            "\n\n**Current settings:**"
            + box("\n".join(f"{x[0]}: {x[1]}" for x in relevant_data), lang="yaml")
        )
        await ctx.send(message)

        check = lambda x: x.channel == ctx.channel and x.author == ctx.author

        try:
            content = await self.bot.wait_for("message", timeout=500, check=check)
        except asyncio.TimeoutError:
            with contextlib.suppress(discord.NotFound):
                await message.delete()

        content = content.content
        valid = validator(cleanup_code(content))

        if not valid:
            return await ctx.send(
                _(
                    "Please provide valid YAML. You can validate your raffle YAML using `{}raffle parse`.".format(
                        ctx.clean_prefix
                    )
                )
            )

        valid["name"] = raffle

        try:
            parser = RaffleManager(valid)
            parser.parser(ctx)
        except RaffleError as e:
            exc = cross(_("An exception occured whilst parsing your data."))
            return await ctx.send(exc + format_traceback(e))

        data = {
            "owner": raffle_data.get("owner"),
            "entries": raffle_data.get("entries"),
        }

        if raffle_data.get("created_at", None):
            data["created_at"] = raffle_data["created_at"]

        conditions = {
            "end_message": valid.get("end_message", None),
            "join_message": valid.get("join_message", None),
            "account_age": valid.get("account_age", None),
            "server_join_age": valid.get("server_join_age", None),
            "roles_needed_to_enter": valid.get("roles_needed_to_enter", None),
            "badges_needed_to_enter": valid.get("badges_needed_to_enter", None),
            "prevented_users": valid.get("prevented_users", None),
            "allowed_users": valid.get("allowed_users", None),
            "description": valid.get("description", None),
            "maximum_entries": valid.get("maximum_entries", None),
            "on_end_action": valid.get("on_end_action", None),
        }

        for k, v in conditions.items():
            if v:
                data[k] = v

        async with self.config.guild(ctx.guild).raffles() as r:
            r[raffle] = data

        additions = []
        deletions = []
        changes = []

        for k, v in conditions.items():
            if v and not existing_data[k]:
                additions.append(k)
                continue
            if not v and existing_data[k]:
                deletions.append(k)
                continue
            if v != existing_data[k]:
                changes.append(k)
                continue

        if any([additions, deletions, changes]):
            message = ""
            if additions:
                message += _("Added:\n") + "\n".join(f"+ {a}" for a in additions)
            if changes:
                message += _("\n\nEdited:\n") + "\n".join(f"> {c}" for c in changes)
            if deletions:
                message += _("\n\nRemoved:\n") + "\n".join(f"- {d}" for d in deletions)

            diffs = box(message, lang="diff")
            update = tick(_("Raffle edited. {}".format(diffs)))

        else:
            update = tick(_("No changes were made."))

        await ctx.send(update)

        await self.replenish_cache(ctx)

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

        await self.replenish_cache(ctx)

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

        await self.replenish_cache(ctx)

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
                message = _("Prevented users list cleared for this raffle.")
                try:
                    await message.edit(content=message)
                except discord.NotFound:
                    await ctx.send(message)

            else:
                await ctx.send(_("No changes have been made."))

    @edit.group()
    async def badges(self, ctx):
        """Manage required badges in a raffle."""
        pass

    @badges.command(name="add")
    async def badges_add(self, ctx, raffle: RaffleFactoryConverter, *badges: str):
        """Add a badge to the required badges list of a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<badges>` - The badge(s) to add to the required badges list.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            badges_list = raffle_data.get("badges_needed_to_enter", [])

            for badge in badges:
                if badge not in VALID_USER_BADGES:
                    return await ctx.send(
                        _('"{}" was not a recognized Discord badge.'.format(badge))
                    )
                if badge in badges_list:
                    return await ctx.send(
                        _(
                            'The "{}" badge is already required in this raffle.'.format(
                                format_underscored_text(badge)
                            )
                        )
                    )

                if not badges_list:
                    raffle_data["badges_needed_to_enter"] = list(badges)
                else:
                    badges_list.append(badge)

            await ctx.send(
                _(
                    "Added the following badges as requirements in this raffle: {}.".format(
                        ", ".join(inline(format_underscored_text(b)) for b in badges)
                    )
                )
            )

        await self.replenish_cache(ctx)

    @badges.command(name="remove", aliases=["del"])
    async def badges_remove(self, ctx, raffle: RaffleFactoryConverter, *badges: str):
        """Remove a badge from the required badges list of a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<member>` - The badge to remove from the required badges list.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            badges_list = raffle_data.get("badges_needed_to_enter", [])

            for badge in badges:
                if badge not in VALID_USER_BADGES:
                    return await ctx.send(
                        _('"{}" was not a recognized Discord badge.'.format(badge))
                    )
                if badge not in badges_list:
                    return await ctx.send(
                        _('The "{}" badge was not already required in this raffle.'.format(badge))
                    )

            badges_list.remove(badge)
            if not badges_list:
                del raffle_data["badges_list"]
            await ctx.send(
                _(
                    "Added the following badges as requirements in this raffle: {}.".format(
                        ", ".join(inline(format_underscored_text(b)) for b in badges)
                    )
                )
            )

        await self.replenish_cache(ctx)

    @badges.command(name="clear")
    async def badges_clear(self, ctx, raffle: RaffleFactoryConverter):
        """Clear the required badges list for a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            badges_list = raffle_data.get("badges_needed_to_enter", None)

            if badges_list is None:
                return await ctx.send(_("There are no required badges."))

            del raffle_data["badges_needed_to_enter"]
            message = _("Required bages list cleared for this raffle.")

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

        await self.replenish_cache(ctx)

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

        await self.replenish_cache(ctx)

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
            try:
                await message.edit(content=_("Allowed list cleared for this raffle."))
            except discord.NotFound:
                await ctx.send(_("Allowed list cleared for this raffle."))

        else:
            await ctx.send(_("No changes have been made."))

        await self.replenish_cache(ctx)

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

        await self.replenish_cache(ctx)

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

        await self.replenish_cache(ctx)

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
                message = "Role requirement list cleared for this raffle."
                try:
                    await message.edit(content=message)
                except discord.NotFound:
                    await ctx.send(message)

            else:
                await ctx.send(_("No changes have been made."))

            await self.replenish_cache(ctx)
