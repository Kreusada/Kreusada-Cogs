import asyncio
import contextlib
import random

import discord
from redbot.core import commands
from redbot.core.commands import Context
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import humanize_list, pagify

from ..mixins.abc import RaffleMixin
from ..mixins.metaclass import MetaClass
from ..utils.checks import account_age_checker, server_join_age_checker
from ..utils.converters import RaffleExists, RaffleFactoryConverter
from ..utils.helpers import format_underscored_text, has_badge
from ..utils.safety import RaffleSafeMember

_ = Translator("Raffle", __file__)


class EventCommands(RaffleMixin, metaclass=MetaClass):
    """All the raffle event leading commands."""

    @commands.group()
    async def raffle(self, ctx: Context):
        pass

    @raffle.command()
    async def draw(self, ctx: Context, raffle: RaffleFactoryConverter):
        """Draw a raffle and select a winner.

        **Arguments:**
            - `<raffle>` - The name of the raffle to draw a winner from.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            raffle_entities = lambda x: raffle_data.get(x, None)

            if not raffle_entities("entries"):
                return await ctx.send(_("There are no participants yet for this raffle."))

            winner = random.choice(raffle_entities("entries"))

            message = raffle_entities("end_message")
            if message:
                if isinstance(message, list):
                    message = random.choice(message)
            else:
                message = _(r"Congratulations {winner.mention}, you have won the {raffle} raffle!")

            on_end_action = raffle_entities("on_end_action") or "keep_winner"
            message = message.format(
                winner=RaffleSafeMember(self.bot.get_user(winner), "winner"), raffle=raffle
            )

            # Let's add a bit of suspense, shall we? :P
            await ctx.send(_("Picking a winner from the pool..."))
            await ctx.trigger_typing()
            await asyncio.sleep(raffle_data.get("suspense_timer", 2))

            await ctx.send(message)

            if on_end_action == "remove_winner":
                raffle_entities("entries").remove(winner)
            elif on_end_action == "keep_winner":
                pass
            elif on_end_action == "remove_and_prevent_winner":
                raffle_entities("entries").remove(winner)
                if raffle_entities("prevented_users"):
                    raffle_entities("prevented_users").append(winner)
                else:
                    raffle_data["prevented_users"] = [winner]
            else:
                # end
                r.pop(raffle)

        await self.clean_guild_raffles(ctx)

    @raffle.command()
    async def kick(self, ctx: Context, raffle: RaffleFactoryConverter, member: discord.Member):
        """Kick a member from your raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
            - `<member>` - The member to kick from the raffle.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            raffle_entities = lambda x: raffle_data.get(x)

            if member.id not in raffle_entities("entries"):
                return await ctx.send(_("This user has not entered this raffle."))

            raffle_entities("entries").remove(member.id)
            await ctx.send(_("User removed from the raffle."))

        await self.clean_guild_raffles(ctx)

    @raffle.command()
    async def join(self, ctx: Context, raffle: RaffleExists):
        """Join a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle to join.
        """
        r = await self.config.guild(ctx.guild).raffles()
        raffle_data = r.get(raffle, None)

        raffle_entities = lambda x: raffle_data.get(x, None)

        if ctx.author.id in raffle_entities("entries"):
            return await ctx.send(_("You are already in this raffle."))

        if raffle_entities("prevented_users") and ctx.author.id in raffle_entities(
            "prevented_users"
        ):
            return await ctx.send(_("You are not allowed to join this particular raffle."))

        if raffle_entities("allowed_users") and ctx.author.id not in raffle_entities(
            "allowed_users"
        ):
            return await ctx.send(_("You are not allowed to join this particular raffle"))

        if ctx.author.id == raffle_entities("owner"):
            return await ctx.send(_("You cannot join your own raffle."))

        if raffle_entities("maximum_entries") and len(
            raffle_entities("entries")
        ) > raffle_entities("maximum_entries"):
            return await ctx.send(
                _("Sorry, the maximum number of users have entered this raffle.")
            )

        if raffle_entities("roles_needed_to_enter"):
            for r in raffle_entities("roles_needed_to_enter"):
                if not r in [x.id for x in ctx.author.roles]:
                    return await ctx.send(
                        _(
                            "You are missing a required role: {}".format(
                                ctx.guild.get_role(r).mention
                            )
                        )
                    )

        if raffle_entities("account_age") and not account_age_checker(
            raffle_entities("account_age")
        ):
            return await ctx.send(
                _(
                    "Your account must be at least {} days old to join.".format(
                        raffle_entities("account_age")
                    )
                )
            )

        if raffle_entities("server_join_age") and not server_join_age_checker(
            ctx, raffle_entities("server_join_age")
        ):
            return await ctx.send(
                _(
                    "You must have been in this guild for at least {} days to join.".format(
                        raffle_entities("server_join_age")
                    )
                )
            )

        if raffle_entities("badges_needed_to_enter"):
            for badge in raffle_entities("badges_needed_to_enter"):
                if not has_badge(badge, ctx.author):
                    return await ctx.send(
                        _(
                            'You must have the "{}" Discord badge to join.'.format(
                                format_underscored_text(badge)
                            )
                        )
                    )

        async with self.config.guild(ctx.guild).raffles() as r:
            raffle_entities = lambda x: r[raffle].get(x, None)
            raffle_entities("entries").append(ctx.author.id)

        welcome_msg = _("{} you have been added to the raffle.".format(ctx.author.mention))

        join = raffle_entities("join_message")
        if join:
            if isinstance(join, list):
                join = random.choice(join)
            join_message = join.format(
                user=RaffleSafeMember(ctx.author, "user"),
                raffle=raffle,
                entry_count=len(raffle_entities("entries")),
            )
            welcome_msg += "\n---\n{}".format(join_message)

        await ctx.send(welcome_msg)
        await self.clean_guild_raffles(ctx)

    @raffle.command()
    async def leave(self, ctx: Context, raffle: RaffleExists):
        """Leave a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle to leave.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            raffle_entries = raffle_data.get("entries")

            if not ctx.author.id in raffle_entries:
                return await ctx.send(_("You are not entered into this raffle."))

            raffle_entries.remove(ctx.author.id)
            await ctx.send(
                _("{0.mention} you have been removed from the raffle.".format(ctx.author))
            )

        await self.clean_guild_raffles(ctx)

    @raffle.command()
    async def mention(self, ctx: Context, raffle: RaffleFactoryConverter):
        """Mention all the users entered into a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle to mention all the members in.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

            raffle_entities = lambda x: raffle_data.get(x)

            if not raffle_entities("entries"):
                return await ctx.send(_("There are no entries yet for this raffle."))

            for page in pagify(
                humanize_list([self.bot.get_user(u).mention for u in raffle_entities("entries")])
            ):
                await ctx.send(page)

        await self.clean_guild_raffles(ctx)

    @raffle.command()
    async def end(self, ctx: Context, raffle: RaffleFactoryConverter):
        """End a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle to end.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            msg = await ctx.send(_("Ending the `{raffle}` raffle...".format(raffle=raffle)))

            r.pop(raffle)

        await asyncio.sleep(1)
        with contextlib.suppress(discord.NotFound):
            await msg.edit(content=_("Raffle ended."))

        await self.clean_guild_raffles(ctx)
