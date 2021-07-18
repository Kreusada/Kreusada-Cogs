import discord
from redbot.core import commands
from redbot.core.commands import Context
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import box, pagify

from ..mixins.abc import RaffleMixin
from ..mixins.metaclass import MetaClass
from ..utils.converters import RaffleExists
from ..utils.enums import RaffleComponents
from ..utils.formatting import CURRENT_PAGE, LEFT_ARROW, RIGHT_ARROW, curl
from ..utils.helpers import compose_menu, format_underscored_text, listumerate, yield_sectors
from ..utils.parser import RaffleManager
from ..version_handler import VersionHandler

_ = Translator("Raffle", __file__)


class InformationalCommands(RaffleMixin, metaclass=MetaClass):
    """Informational commands."""

    @commands.group()
    async def raffle(self, ctx: Context):
        pass

    @raffle.command()
    async def info(self, ctx: Context, raffle: RaffleExists):
        """Get information about a certain raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle to get information for.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

        quotes = lambda x: f'"{x}"'
        relevant_data = []
        for k, v in sorted(raffle_data.items(), key=lambda x: len(x[0])):
            if k in ("owner", "entries", "created_at", "name", "description"):
                # These are not user defined keys
                continue
            if isinstance(v, str):
                v = quotes(v)
            relevant_data.append((k, v))

        pre_determined = {
            "raffle": quotes(raffle),
            "description": raffle_data.get("description", None) or "No description was provided.",
            "owner": str(ctx.guild.get_member(raffle_data["owner"])),
            "created_at": raffle_data.get("created_at", None),
            "entries": len(raffle_data["entries"]) or "No entries yet.",
        }

        message = ""
        for k, v in pre_determined.items():
            if v is None:
                continue
            message += f"\n{k.capitalize()}: {v!s}"
        if relevant_data:
            message += "\n\n"

        for page in pagify(
            _(message + "\n".join(f"{x[0]}: {x[1]}" for x in relevant_data)), page_length=1975
        ):
            await ctx.send(box(page, lang="yaml"))

        await self.clean_guild_raffles(ctx)

    @raffle.command()
    async def asyaml(self, ctx: Context, raffle: RaffleExists):
        """Get a raffle in its YAML format.

        **Arguments:**
            - `<raffle>` - The name of the raffle to get the YAML for.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)

        quotes = lambda x: f'"{x}"'
        relevant_data = [("name", quotes(raffle))]
        for k, v in raffle_data.items():
            if k in ("owner", "entries", "created_at"):
                # These are not user defined keys
                continue
            if isinstance(v, str):
                v = quotes(v)
            relevant_data.append((k, v))

        message = _("**YAML Format for the `{}` raffle**\n".format(raffle))
        await ctx.send(
            message + box("\n".join(f"{x[0]}: {x[1]}" for x in relevant_data), lang="yaml")
        )

        await self.clean_guild_raffles(ctx)

    @raffle.command(name="list")
    async def _list(self, ctx: Context):
        """List the currently ongoing raffles."""
        r = await self.config.guild(ctx.guild).raffles()

        if not r:
            return await ctx.send(_("There are no ongoing raffles."))

        lines = []
        for k, v in sorted(r.items()):
            description = v.get("description", None)
            if not description:
                description = ""
            lines.append("**{}** {}".format(k, RaffleManager.shorten_description(description)))

        embeds = []
        data = list(pagify("\n".join(lines), page_length=1024))

        for index, page in enumerate(data, 1):
            embed = discord.Embed(
                title=_("Current raffles"), description=page, color=await ctx.embed_colour()
            )
            embed.set_footer(text="Page {}/{}".format(index, len(data)))
            embeds.append(embed)

        await compose_menu(ctx, embeds)
        await self.clean_guild_raffles(ctx)

    @raffle.command()
    async def raw(self, ctx: Context, raffle: RaffleExists):
        """View the raw dictionary for a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle.
        """
        r = await self.config.guild(ctx.guild).raffles()
        for page in pagify(str({raffle: r[raffle]}), page_length=1985):
            await ctx.send(box(page, lang="json"))

        await self.clean_guild_raffles(ctx)

    @raffle.command()
    async def members(self, ctx: Context, raffle: RaffleExists):
        """Get all the members of a raffle.

        **Arguments:**
            - `<raffle>` - The name of the raffle to get the members from.
        """
        r = await self.config.guild(ctx.guild).raffles()

        raffle_data = r.get(raffle, None)

        entries = raffle_data.get("entries")

        if not entries:
            return await ctx.send(_("There are no entries yet for this raffle."))

        embed_pages = []

        if len(entries) == 1:
            entry_grammar = _("entry")
        else:
            entry_grammar = _("entries")
        for chunk in list(yield_sectors(listumerate(entries, 1), 10)):
            message = ""
            for c, v in chunk:
                message += f"#{c} {ctx.guild.get_member(v) or 'Unknown User'}\n"
            embed = discord.Embed(
                description=box(message, lang="md"), color=await ctx.embed_colour()
            )
            embed.set_author(
                name=f"{raffle} | {len(entries)} {entry_grammar}",
                icon_url=self.bot.user.avatar_url,
            )
            embed.set_footer(text="Sorted in order of join time.")
            embed_pages.append(embed)

        await compose_menu(ctx, embed_pages)
        await self.clean_guild_raffles(ctx)

    @raffle.command()
    async def conditions(self, ctx: Context):
        """Get information about how conditions work."""
        pages = []
        sorted_components = sorted(RaffleComponents, key=lambda x: x.name)
        sorted_names = [component.name for component in sorted_components]

        for c, v in enumerate(sorted_components, 1):
            condition = v.name
            properties = v.value

            info = (
                f"Qualified name: [{condition}]\n"
                f"Supported types: [{', '.join(v.__name__ for v in properties['supported_types'])}]\n"
                f"Potential exceptions: [{', '.join(v.__name__ for v in properties['potential_exceptions'])}]\n"
            )

            if properties["required_condition"]:
                emoji = "\N{WHITE HEAVY CHECK MARK}"
            else:
                emoji = "\N{CROSS MARK}"
            info += f"Required condition: [{emoji}]"

            try:
                next_condition = sorted_names[c]
            except IndexError:
                next_condition = sorted_names[0]

            try:
                prev_condition = sorted_names[c - 2]
            except IndexError:
                prev_condition = sorted_names[-1]

            embed = discord.Embed(
                title=f"Condition #{c}/{len(RaffleComponents)}: {format_underscored_text(condition)}",
                color=await ctx.embed_colour(),
            )

            embed.add_field(
                name="Description",
                value=box(f"{v.name} =\n\n{properties['description']}", lang="fix"),
                inline=False,
            )

            embed.add_field(name="Information", value=box(info, lang="yaml"), inline=False)

            if properties["variables"] is not None:
                variables = []
                for var in properties["variables"]:
                    # Only conditions with variables atm is join_message and end_message
                    condition_switch = {
                        "join_message": "user",
                        "end_message": "winner",
                    }
                    if "__" in var:
                        var = f"{condition_switch[condition]}.{var.split('__')[-1]}"
                    variables.append(curl(var))

                embed.add_field(
                    name="Variables",
                    value=box("\n".join(f"! {v}" for v in variables), lang="diff"),
                )

            example = properties["example"]
            if isinstance(example, str):
                example = '"{}"'.format(example)
            embed.add_field(
                name="Example Usage",
                value=box(f"{condition}: {example}", lang="yaml"),
                inline=False,
            )
            embed.set_footer(
                text=(
                    f"{LEFT_ARROW} {prev_condition}\n"
                    f"{CURRENT_PAGE} {condition}\n"
                    f"{RIGHT_ARROW} {next_condition}"
                )
            )
            pages.append(embed)
        await compose_menu(ctx, pages)
        await self.clean_guild_raffles(ctx)

    @raffle.command()
    async def version(self, ctx: Context):
        """Get the version of your Raffle cog."""
        async with ctx.typing():
            cls = VersionHandler()
            raw = await cls.request_raw_version()
            if not await cls.validate():
                message = _(
                    "**Your raffle cog is out of date!**\n"
                    "The up to date version is **{1}**, whilst yours is **{0.__version__}**.\n\n"
                    "Consider updating through `{2}cog update raffle`."
                )
            else:
                message = _("Version: **{0.__version__}**")

        await ctx.send(message.format(self, cls.tuple_to_str(raw), ctx.clean_prefix))

    @raffle.command()
    async def docs(self, ctx: Context):
        """Get a link to the docs."""
        message = _("**Docs:** {0.docs}".format(self))
        await ctx.send(message)
