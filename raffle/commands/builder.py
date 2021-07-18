import asyncio
import contextlib
from typing import Optional

import discord
from redbot.core import commands
from redbot.core.commands import Context
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import box

from ..mixins.abc import RaffleMixin
from ..mixins.metaclass import MetaClass
from ..utils.enums import RaffleComponents
from ..utils.exceptions import RaffleError
from ..utils.formatting import cross, tick
from ..utils.helpers import cleanup_code, format_traceback, getstrftime, number_suffix, validator
from ..utils.parser import RaffleManager

_ = Translator("Raffle", __file__)


class BuilderCommands(RaffleMixin, metaclass=MetaClass):
    """Mixin for commands under ``[p]raffle edit``."""

    @commands.group()
    async def raffle(self, ctx: Context):
        pass

    @raffle.group()
    async def create(self, ctx: Context):
        """Create a raffle."""
        pass

    @create.command(name="complex")
    async def _complex(self, ctx: Context):
        """Create a raffle with complex conditions."""
        await ctx.trigger_typing()
        check = lambda x: x.author == ctx.author and x.channel == ctx.channel
        message = _(
            "You're about to create a new raffle.\n"
            "Please consider reading the docs about the various "
            "conditional blocks if you haven't already.\n\n" + self.docs
        )

        message += _("\n\n**Conditions Blocks:**") + box(
            "\n".join(f"+ {e.name}" for e in RaffleComponents), lang="diff"
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
            return await ctx.send(
                cross(
                    _(
                        "Please provide valid YAML. You can validate your raffle YAML using `{}raffle parse`."
                    )
                ).format(ctx.clean_prefix)
            )

        try:
            parser = RaffleManager(valid)
            parser.parser(ctx)
        except RaffleError as e:
            exc = cross(_("An exception occured whilst parsing your data."))
            return await ctx.send(exc + format_traceback(e))

        async with self.config.guild(ctx.guild).raffles() as raffle:

            rafflename = valid.get("name").lower()

            if rafflename in [x.lower() for x in raffle.keys()]:
                return await ctx.send(_("A raffle with this name already exists."))

            datetimeinfo = _(
                "{day} of {month}, {year} ({time})".format(
                    day=number_suffix(getstrftime("d")),
                    month=getstrftime("B"),
                    year=getstrftime("Y"),
                    time=getstrftime("X"),
                )
            )

            data = {
                "entries": [],
                "owner": ctx.author.id,
                "created_at": datetimeinfo,
            }

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

            raffle[rafflename] = data
            await ctx.send(tick(_("Raffle created with the name `{}`.".format(rafflename))))

        await self.clean_guild_raffles(ctx)

    @create.command()
    async def simple(self, ctx, raffle_name: str, *, description: Optional[str] = None):
        """Create a simple arguments with just a name and description.

        **Arguments:**
            - `<name>` - The name for the raffle.
            - `[description]` - The description for the raffle.
        """
        raffle_name = raffle_name.lower()
        async with self.config.guild(ctx.guild).raffles() as raffle:

            if raffle_name in [x.lower() for x in raffle.keys()]:
                return await ctx.send(_("A raffle with this name already exists."))

            datetimeinfo = _(
                "{day} of {month}, {year} ({time})".format(
                    day=number_suffix(getstrftime("d")),
                    month=getstrftime("B"),
                    year=getstrftime("Y"),
                    time=getstrftime("X"),
                )
            )

            data = {
                "entries": [],
                "owner": ctx.author.id,
                "created_at": datetimeinfo,
            }

            if description:
                data["description"] = description

            raffle[raffle_name] = data
        await ctx.send(tick(_("Raffle created with the name `{}`.".format(raffle_name))))
        await self.clean_guild_raffles(ctx)
