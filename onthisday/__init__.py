"""The OnThisDay module. Find out what happened on a certain day, in multiple different years in history."""

import asyncio
import datetime
import re
from random import choice
from typing import Dict, Iterable, Optional, Union

import aiohttp
import dateparser
import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands import BadArgument, Context, Converter
from redbot.core.utils import get_end_user_data_statement
from redbot.core.utils.chat_formatting import inline, warning

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)

ENDPOINT = "https://byabbe.se/on-this-day/{}/events.json"

DEFAULT_DESCRIPTION = """
Please send a valid year from the list of years below.
These are the most significant years for events occuring
on this day. Only years above 0 are included.
"""

MONTH_MAPPING = {
    "1": "january",
    "2": "february",
    "3": "march",
    "4": "april",
    "5": "may",
    "6": "june",
    "7": "july",
    "8": "august",
    "9": "september",
    "10": "october",
    "11": "november",
    "12": "december",
}


def highlight_numerical_data(string):
    return re.sub(r"(([\d{1}],?)+)", r"**\1**", string)


def retrieve_above_0(year):
    return year.strip().isdigit()


def columns(years):
    m = f"{chr(12644)}\n"  # padding
    f = lambda s: inline(s.zfill(4))
    for x in range(6, len(years), 6):
        m += "\n" + (" " * 5).join(map(f, years[x - 6 : x]))
    return m


def date_suffix(number) -> str:
    number = int(number)
    suffixes = {0: "th", 1: "st", 2: "nd", 3: "rd"}
    for i in range(4, 10):
        suffixes[i] = "th"
    return str(number) + suffixes[int(str(number)[-1])]


def now() -> datetime.datetime:
    return datetime.datetime.now()


def current_year() -> int:
    return datetime.date.today().year


def yield_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


class DateConverter(Converter):
    """Date converter which uses dateparser.parse()."""

    async def convert(self, ctx: Context, arg: str) -> datetime.datetime:
        parsed = dateparser.parse(arg)
        if parsed is None:
            raise BadArgument("Unrecognized date/time.")
        if parsed.strftime("%Y") != str(now().strftime("%Y")):
            raise BadArgument("Please do not specify a year.")
        return parsed


class YearDropdown(discord.ui.Select):
    def __init__(self, otd: "OnThisDay", /):
        self.otd = otd
        cy = current_year()
        options = [
            discord.SelectOption(
                label=year,
                description=f"On this day, {cy - int(year)} years ago",
                emoji="\N{CLOCK FACE THREE OCLOCK}",
            )
            for year in self.otd.year_data
            if int(year) in self.otd.year_range
        ]

        super().__init__(placeholder="Choose a year...", options=options)

    async def callback(self, interaction: discord.Interaction):
        await self.otd.display_events(
            interaction,
            year=self.values[0],
        )


class YearDropdownView(discord.ui.View):
    def __init__(self, otd: "OnThisDay"):
        super().__init__()
        self.add_item(YearDropdown(otd))


class YearRangeDropdown(discord.ui.Select):
    """This exists because the number of years dispatched always
    exceeds the Select options cap of 25.
    """

    YEAR_RANGES = [
        range(1901),
        range(1901, 1951),
        range(1951, 2001),
        range(2001, current_year() + 1),
    ]

    YEAR_RANGES_HUMANIZED = ["0 - 1900", "1901 - 1950", "1951 - 2000", "2001 - present"]

    def __init__(self, otd: "OnThisDay", /):
        self.otd = otd

        emojis = [
            "\N{LARGE RED CIRCLE}",
            "\N{LARGE ORANGE CIRCLE}",
            "\N{LARGE YELLOW CIRCLE}",
            "\N{LARGE GREEN CIRCLE}",
        ]

        options = [
            discord.SelectOption(
                label=self.YEAR_RANGES_HUMANIZED[i],
                value=i,
                description=f"Get choice from {self.YEAR_RANGES_HUMANIZED[i].replace('-', 'to')}",
                emoji=emojis[i],
            )
            for i in range(4)
        ]

        super().__init__(placeholder="Choose a year range...", options=options)

    async def callback(self, interaction: discord.Interaction):
        self.otd.year_range = self.YEAR_RANGES[int(self.values[0])]
        await interaction.response.edit_message(
            content=f"Selected year range: **{self.YEAR_RANGES_HUMANIZED[int(self.values[0])]}**\nSelect a year from the list of available years.",
            view=YearDropdownView(self.otd),
        )


class YearRangeDropdownView(discord.ui.View):
    def __init__(self, otd: "OnThisDay"):
        super().__init__()
        self.add_item(YearRangeDropdown(otd))


class ButtonView(discord.ui.View):
    def __init__(self, buttons: dict[str, str]):
        super().__init__()
        for label, url in buttons.items():
            self.add_item(discord.ui.Button(label=label, url=url))


class OnThisDay(commands.Cog):
    """Find out what happened on a certain day, in multiple different years in history."""

    __version__ = "2.0.0"
    __author__ = "Kreusada"

    def __init__(self, bot: Red):
        self.bot = bot
        self.session = aiohttp.ClientSession()
        self.date_number: Optional[str] = None
        self.month_number: Optional[str] = None
        self.year: Optional[str] = None
        self.year_data = {}
        self.year_range: Optional[range] = None
        self.date_wiki: Optional[str] = None

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    async def cog_unload(self) -> None:
        await self.session.close()

    async def display_events(
        self,
        ctx: Union[commands.Context, discord.Interaction],
        *,
        year: str,
    ):
        event = self.year_data[year]
        years_ago = int(self.year) - int("".join(filter(str.isdigit, year)))
        content = (
            event["content"]
            + "\n\n"
            + f"This event occured on the __{date_suffix(self.date_number)} of {MONTH_MAPPING[self.month_number].capitalize()}, {year}__."
        )
        embed = discord.Embed(
            title=f"On this day, {years_ago} years ago...",
            description=highlight_numerical_data(content),
            color=await self.bot.get_embed_colour(ctx.channel),
        )
        embed.set_footer(text="See the below links for related wikipedia articles")
        _d = {
            f"The year '{year}'": "https://en.wikipedia.org/wiki/" + year,
            f"The date '{self.date_number.zfill(2)}/{self.month_number.zfill(2)}'": self.date_wiki,
        }
        embed.add_field(
            name="Other significant events",
            value="\n".join(f"- [{k}]({v})" for k, v in _d.items()),
            inline=False,
        )
        wiki_dict = {w["title"]: w["wikipedia"] for w in event["wikipedia"]}
        if isinstance(ctx, discord.Interaction):
            send_method = ctx.response.edit_message
        else:
            send_method = ctx.send
        await send_method(content=None, embed=embed, view=ButtonView(wiki_dict))

    async def run_otd(
        self,
        ctx: commands.Context,
        date: Optional[datetime.datetime],
        random: bool = False,
    ):
        self.cache_date(date)
        try:
            async with self.session.get(
                ENDPOINT.format(f"{self.month_number}/{self.date_number}")
            ) as session:
                if session.status != 200:
                    return await ctx.maybe_send_embed(
                        warning("An error occured whilst retrieving information for this day.")
                    )
                content = await session.json()
        except aiohttp.ClientError:
            return await ctx.maybe_send_embed(
                warning("An error occured whilst retrieving information for this day.")
            )
        else:
            self.date_wiki = content["wikipedia"]
            events = filter(lambda x: retrieve_above_0(x["year"]), content["events"])
            data = {
                e["year"]: {"content": e["description"], "wikipedia": e["wikipedia"]}
                for e in events
            }
            self.year_data = data
            if random:
                await self.display_events(ctx, year=choice(list(data.keys())))
            else:
                await ctx.send(
                    "Choose a year range to select from:",
                    view=YearRangeDropdownView(self),
                )

    def cache_date(self, date: Optional[datetime.datetime], /) -> Dict[str, int]:
        if date is None:
            date = now()

        self.month_number = date.strftime(r"%m").lstrip("0")
        self.date_number = date.strftime(r"%d").lstrip("0")
        self.year = date.strftime(r"%Y")

    @commands.has_permissions(embed_links=True)
    @commands.group(invoke_without_command=True, aliases=["otd"])
    async def onthisday(self, ctx: commands.Context, *, date: DateConverter = None):
        """Find out what happened on this day, in various different years!

        If you want to specify your own date, you can do so by using
        `[p]onthisday [date]`.
        You can also receive a random year by using `[p]onthisday random [day]`.
        """
        await ctx.typing()
        await self.run_otd(ctx, date=date, random=False)

    @onthisday.command()
    async def random(self, ctx: commands.Context, *, date: DateConverter = None):
        """Find out what happened on this day, in a random year.

        If you want to specify your own date, you can do so by using
        `[p]onthisday [date]`.
        """
        await ctx.typing()
        await self.run_otd(ctx, date=date, random=True)


async def setup(bot: Red):
    await bot.add_cog(OnThisDay(bot))
