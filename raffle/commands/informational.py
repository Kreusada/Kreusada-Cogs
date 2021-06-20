import discord
import pathlib

from redbot.core import commands
from redbot.core.commands import Context
from redbot.core.i18n import Translator
from redbot.core.utils.chat_formatting import box, pagify, humanize_list

from ..mixins.abc import RaffleMixin
from ..enums import RaffleComponents
from ..helpers import format_dashed_title, compose_menu
from ..version_handler import VersionHandler
from ..parser import RaffleManager


_ = Translator("Raffle", __file__)

class InformationalCommands(RaffleMixin):
    """Informational commands."""
    

    @commands.group()
    async def raffle(self, ctx: Context):
        pass


    @raffle.command()
    async def info(self, ctx: Context, raffle: str):
        """Get information about a certain raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle to get information for.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send(_("There is not an ongoing raffle with the name `{}`.".format(raffle)))

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
            "owner": str(ctx.guild.get_member(raffle_data['owner'])),
            "created_at": raffle_data.get("created_at", None),
            "entries": len(raffle_data['entries']) or "No entries yet.",
        }

        message = format_dashed_title(pre_determined)
        for k, v in pre_determined.items():
            if v is None:
                continue
            message += f"\n{k.capitalize()}: {v!s}"
        if relevant_data:
            message += "\n" + format_dashed_title(pre_determined) + "\n"
        
        for page in pagify(_(message + "\n".join(f"{x[0]}: {x[1]}" for x in relevant_data)), page_length=1975):
            await ctx.send(box(page, lang="yaml"))

        await self.replenish_cache(ctx)


    @raffle.command()
    async def asyaml(self, ctx: Context, raffle: str):
        """Get a raffle in its YAML format.

        **Arguments:**
            - `<raffle>` - The name of the raffle to get the YAML for.
        """
        async with self.config.guild(ctx.guild).raffles() as r:

            raffle_data = r.get(raffle, None)
            if not raffle_data:
                return await ctx.send(_("There is not an ongoing raffle with the name `{}`.".format(raffle)))

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
        await ctx.send(message + box("\n".join(f"{x[0]}: {x[1]}" for x in relevant_data), lang="yaml"))

        await self.replenish_cache(ctx)


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
                description=""
            lines.append("**{}** {}".format(k, RaffleManager.shorten_description(description)))

        embeds = []
        data = list(pagify("\n".join(lines), page_length=1024))

        for index, page in enumerate(data, 1):
            embed = discord.Embed(
                title=_("Current raffles"),
                description=page,
                color=await ctx.embed_colour()
            )
            embed.set_footer(text="Page {}/{}".format(index, len(data)))
            embeds.append(embed)

        await compose_menu(ctx, embeds)
        await self.replenish_cache(ctx)


    @raffle.command()
    async def raw(self, ctx: Context, raffle: str):
        """View the raw dictionary for a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle.
        """
        r = await self.config.guild(ctx.guild).raffles()

        raffle_data = r.get(raffle, None)
        if not raffle_data:
            return await ctx.send(_("There is not an ongoing raffle with the name `{}`.".format(raffle)))

        for page in pagify(str({raffle: raffle_data})):
            await ctx.send(box(page, lang="json"))

        await self.replenish_cache(ctx)


    @raffle.command()
    async def members(self, ctx: Context, raffle: str):
        """Get all the members of a raffle.
        
        **Arguments:**
            - `<raffle>` - The name of the raffle to get the members from.
        """
        r = await self.config.guild(ctx.guild).raffles()

        raffle_data = r.get(raffle, None)
        if not raffle_data:
            return await ctx.send(_("There is not an ongoing raffle with the name `{}`.".format(raffle)))

        entries = raffle_data.get("entries")

        if not entries:
            return await ctx.send(_("There are no entries yet for this raffle."))

        embed_pages = []

        if len(entries) == 1:
            entry_grammar = _("entry")
        else:
            entry_grammar = _("entries")
            for page in pagify(humanize_list([self.bot.get_user(u).display_name for u in entries])):
                embed = discord.Embed(
                    description=page,
                    color=await ctx.embed_colour()
                )
        embed.title = f"{len(entries)} {entry_grammar}"
        embed_pages.append(embed)

        await compose_menu(ctx, embed_pages)
        await self.replenish_cache(ctx)


    @raffle.command()
    async def conditions(self, ctx: Context):
        """Get information about how conditions work."""
        message = "\n".join(f"{e.name}:\n\t{e.value}" for e in RaffleComponents)
        await ctx.send(box(message, lang="yaml"))
        await self.replenish_cache(ctx)


    @raffle.command()
    async def template(self, ctx: Context):
        """Get a template of a raffle."""
        with open(pathlib.Path(__file__).parent / "template.yaml") as f:
            docs = "**For more information:** {}\n".format(self.docs)
            await ctx.send(_(docs + box("".join(f.readlines()), lang="yaml")))


    @raffle.command()
    async def version(self, ctx: Context):
        """Get the version of your Raffle cog."""
        async with ctx.typing():
            cls = VersionHandler()
            raw = await cls.rawversiongetter(True)
            if not await cls.validate():
                message = _(
                    "**Your raffle cog is out of date!**\n"
                    "The up to date version is **{1}**, whilst yours is **{0.__version__}**.\n\n"
                    "Consider updating through `{2}cog update raffle`."
                )
            else:
                message = _("Version: {0.__version__}")

        await ctx.send(message.format(self, raw, ctx.clean_prefix))


    @raffle.command()
    async def docs(self, ctx: Context):
        """Get a link to the docs."""
        message = _("**Docs:** {0.docs}".format(self))
        await ctx.send(message)