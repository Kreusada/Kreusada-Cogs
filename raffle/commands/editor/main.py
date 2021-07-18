import asyncio
import contextlib
from typing import Union

import discord
from redbot.core import commands
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate

from ...mixins.abc import RaffleMixin
from ...mixins.metaclass import MetaClass
from ...utils.converters import RaffleFactoryConverter
from ...utils.enums import RaffleComponents
from ...utils.exceptions import InvalidArgument, RaffleError
from ...utils.formatting import cross, tick
from ...utils.helpers import (
    cleanup_code,
    format_traceback,
    raffle_safe_member_scanner,
    start_interactive_message_session,
    validator,
)
from ...utils.parser import RaffleManager

_ = Translator("Raffle", __file__)


class EditorCommands(RaffleMixin, metaclass=MetaClass):
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

        await self.clean_guild_raffles(ctx)

    @edit.command()
    async def convertsimple(self, ctx, raffle: RaffleFactoryConverter):
        """Convert a raffle to a simple one (name and description).

        **Arguments**
            - `<raffle>` - The name of the raffle.
        """
        components = [e.name for e in RaffleComponents][2:]

        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            message = _(
                ":warning: Are you sure you want to convert this raffle to a simple raffle?\n"
                "It will remove all the conditions!"
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
                await ctx.send(_("You took too long to respond."))

            if predicate.result:
                delkeys = []
                for k in raffle_data.keys():
                    if k in components:
                        delkeys.append(k)
                for k in delkeys:
                    del raffle_data[k]
                await ctx.send(_("Raffle converted to simple raffle."))

            else:
                await ctx.send(_("No changes have been made."))

        await self.clean_guild_raffles(ctx)

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

        await self.clean_guild_raffles(ctx)

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

        await self.clean_guild_raffles(ctx)

    @edit.command()
    async def stimer(self, ctx, raffle: RaffleFactoryConverter, suspense_timer: Union[int, bool]):
        """Edit the suspense timer for a raffle.

        Use `0` or `false` to remove this feature.
        This feature defaults to 2 seconds if not set.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<description>` - The new suspense timer.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            if not suspense_timer:
                with contextlib.suppress(KeyError):
                    del raffle_data["suspense_timer"]
                return await ctx.send(_("Suspense timer reset to the default: 2 seconds."))

            elif suspense_timer is True:
                return await ctx.send(
                    _('Please provide a number, or "false" to disable the description.')
                )

            else:
                if not suspense_timer in [*range(0, 11)]:
                    await ctx.send("New suspense timer must be a number between 0 and 10.")
                raffle_data["suspense_timer"] = suspense_timer
                await ctx.send(_("Suspense timer updated for this raffle."))

        await self.clean_guild_raffles(ctx)

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

        await self.clean_guild_raffles(ctx)

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

        await self.clean_guild_raffles(ctx)

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

        await self.clean_guild_raffles(ctx)

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

        await self.clean_guild_raffles(ctx)

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
            "suspense_timer": raffle_data.get("suspense_timer", None),
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
            "suspense_timer": valid.get("suspense_timer", None),
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

        await self.clean_guild_raffles(ctx)
