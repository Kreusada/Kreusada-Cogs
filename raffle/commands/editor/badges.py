from redbot.core import commands
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import inline

from ...mixins.abc import RaffleMixin
from ...mixins.metaclass import MetaClass
from ...utils.checks import VALID_USER_BADGES
from ...utils.converters import RaffleFactoryConverter
from ...utils.helpers import format_underscored_text

_ = Translator("Raffle", __file__)


class Badges(RaffleMixin, metaclass=MetaClass):
    """Commands used to edit badge requirements for raffles."""

    @commands.group()
    async def raffle(self, *args, **kwargs):
        pass

    @raffle.group()
    async def edit(self, ctx):
        """Edit the settings for a raffle."""
        pass

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

        await self.clean_guild_raffles(ctx)

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

        await self.clean_guild_raffles(ctx)

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
