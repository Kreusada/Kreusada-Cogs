import contextlib
import datetime
import json
import pathlib
import sys
from typing import Dict, Optional, Union

import discord
import pycountry

try:
    import tabulate
except ModuleNotFoundError:
    tabulate = None

from redbot.core import commands
from redbot.core.commands import BadArgument, Cog, Context, Converter
from redbot.core.utils.chat_formatting import box, pagify
from redbot.core.utils.menus import DEFAULT_CONTROLS, close_menu, menu


def square(t):
    return f"[{t}]"


def emojify(t):
    return f":{t}:"


def format_attr(t):
    return t.replace("_", " ").title()


EXCEPTIONS = {"russia": "ru"}
IMAGE_BASE = "https://flagpedia.net/data/flags/w580/{}.png"
SPECIAL_IMAGES = {
    "england": {
        "url": "gb-eng",
        "emoji": "england",
    },
    "wales": {
        "url": "gb-wls",
        "emoji": "wales",
    },
    "scotland": {
        "url": "gb-sct",
        "emoji": "scotland",
    },
    "kosovo": {
        "url": "xk",
        "emoji": "flag_xk",
    },
    "palestine": {
        "url": "ps",
        "emoji": "flag_ps",
    },
}


class CountryConverter(Converter):
    """Convert for country input"""

    async def convert(self, ctx: Context, argument: str) -> Optional[Dict[str, Union[str, int]]]:
        argument = argument.lower()
        get = pycountry.countries.get

        if argument in SPECIAL_IMAGES:
            emoji = SPECIAL_IMAGES[argument]["emoji"]

            if tabulate:
                description = box(f"Emoji Information  [:{emoji}:]", lang="ini")
            else:
                description = box(f"Emoji Information: :{emoji}:", lang="yaml")

            country_name = argument.title()
            image = IMAGE_BASE.format(SPECIAL_IMAGES[argument]["url"])

            return {
                "description": description,
                "emoji": emojify(emoji),
                "name": square(country_name),
                "title": f":{emoji}: {country_name}",
                "image": image,
            }

        obj = get(name=argument) or get(alpha_2=argument)
        if not obj:
            for k, v in EXCEPTIONS.items():
                if k in argument:
                    obj = get(alpha_2=v)
                    break
            if not obj:
                raise BadArgument("Could not match %r to a country." % argument)

        ret = {
            "name": obj.name.title(),
            "title": f":flag_{obj.alpha_2.lower()}: {obj.name}",
            "emoji": f":flag_{obj.alpha_2.lower()}:",
            "image": IMAGE_BASE.format(obj.alpha_2.lower()),
        }

        for attr in ("alpha_2", "alpha_3", "numeric", "official_name"):
            if hasattr(obj, attr):
                ret[attr] = getattr(obj, attr)

        return ret


with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class Flags(Cog):
    """Get flags from country names."""

    __version__ = "1.1.5"
    __author__ = "Kreusada"

    def __init__(self, bot):
        self.bot = bot
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(KeyError):
                self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def flag(self, ctx: Context, *, argument: CountryConverter):
        """Get the flag for a country.

        Either the country name or alpha 2 code can be provided.

        **Examples:**

            - ``[p]flag russia``
            - ``[p]flag brazil``
            - ``[p]flag dk``
            - ``[p]flag se``
        """
        description = argument.get("description", None)
        image = argument.pop("image")
        title = argument.pop("title")

        if description is None:
            if tabulate:
                description = box(
                    tabulate.tabulate(
                        [(format_attr(k), square(v)) for k, v in argument.items()],
                        tablefmt="plain",
                    ),
                    lang="ini",
                )
            else:
                description = box(
                    (f"{format_attr(k)}: {v}" for k, v in argument.items()), lang="yaml"
                )

        embed = discord.Embed(
            title=title,
            description=description,
            color=await ctx.embed_colour(),
            timestamp=datetime.datetime.now(),
        )

        embed.set_image(url=image)
        await menu(ctx, [embed], {"\N{CROSS MARK}": close_menu})

    @commands.command()
    async def flagemojis(self, ctx: commands.Context, *countries: CountryConverter):
        """Get flag emojis for a list of countries.

        **Examples:**

            - ``[p]flagemojis qatar brazil mexico``
            - ``[p]flagemojis "solomon islands" germany``
        """
        if not countries:
            return await ctx.send_help()
        # Here, I am removing duplicates. Cannot do set(countries)
        # because set takes hashable objects of which dict is not
        # using dict.fromkeys() instead of set() to retain insertion order
        unique_countries = [
            dict(s) for s in dict.fromkeys(frozenset(d.items()) for d in countries)
        ]
        message = "\n".join(f"{c['emoji']} - `{c['emoji']}`" for c in unique_countries)
        for page in pagify(message):
            await ctx.send(page)

    @commands.command()
    @commands.has_permissions(embed_links=True)
    async def flags(self, ctx: commands.Context, page_number: int = None):
        """Get a list of all the flags and their alpha 2 codes."""
        embeds = []
        message = "\n".join(
            f":flag_{c.alpha_2.lower()}: `[{c.alpha_2}]` {c.name}" for c in pycountry.countries
        )
        pages = tuple(pagify(message, page_length=500))
        color = await ctx.embed_colour()
        for page in pages:
            embed = discord.Embed(
                title=f"All flags (page {pages.index(page) + 1}/{len(pages)})",
                description=page,
                color=color,
            )
            embeds.append(embed)
        if page_number is not None:
            try:
                embed = embeds[page_number - 1]
            except IndexError:
                await ctx.send(
                    f"Invalid page number provided, must be between 1 and {len(embeds)}."
                )
                return
            else:
                await ctx.send(embed=embed)
        else:
            await menu(ctx, embeds, DEFAULT_CONTROLS)
