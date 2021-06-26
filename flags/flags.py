import contextlib
import datetime
import discord
import pycountry

try:
    import tabulate
except ModuleNotFoundError:
    tabulate = None

from redbot.core import commands
from redbot.core.commands import Cog, Context
from redbot.core.utils.chat_formatting import box, humanize_list


def square(t):
    return f"[{t}]"


def format_attr(t):
    return t.replace('_',' ').title()


class Flags(Cog):
    """Get flags from country names."""
    
    __version__ = "1.0.0"
    __author__ = ["Kreusada"]

    def __init__(self, bot):
        self.bot = bot
        self.image_base = "https://flagpedia.net/data/flags/w580/{}.png"
        self.exceptions = {"russia": "ru"}


    def format_help_for_context(self, ctx: Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = humanize_list(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"


    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return


    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("flags")


    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("flags", lambda x: self)


    @commands.command()
    async def flag(self, ctx: Context, *, argument: str):
        """Get the flag for a country.
        
        Either the country name or alpha 2 code can be provided.
        
        **Examples:**

            - ``[p]flag russia``
            - ``[p]flag brazil``
            - ``[p]flag dk``
            - ``[p]flag se``
        """
        argument = argument.lower()
        get = lambda **kwargs: pycountry.countries.get(**kwargs)

        if argument in ("england", "scotland", "wales"):

            special_images = {
                "england": "gb-eng",
                "wales": "gb-wls",
                "scotland": "gb-sct"
            }

            if tabulate:
                description = box(f"Emoji Information  [:{argument}:]", lang="ini")
            else:
                description = box(f"Emoji Information: :{argument}:", lang="yaml")
            emoji = f":{argument}:"
            country_name = argument.title()
            image = self.image_base.format(special_images[argument])

        else:

            obj = get(name=argument) or get(alpha_2=argument)
            if not obj:
                obj = None
                for k, v in self.exceptions.items():
                    if k in argument:
                        obj = get(alpha_2=v)
                        break
                if not obj:
                    return await ctx.send("Could not match this argument to a country.")

            data = []

            if hasattr(obj, "alpha_2"):
                emoji = f":flag_{obj.alpha_2.lower()}:"
                data.append(("Emoji Information", square(emoji)))

            for attr in ("alpha_2", "alpha_3", "numeric", "official_name"):
                if hasattr(obj, attr):
                    data.append((format_attr(attr), square(getattr(obj, attr))))

            if tabulate:
                description = box(tabulate.tabulate(data, tablefmt="plain"), lang="ini")
            else:
                description = box((f"{v[0]}: {v[1]}" for v in data), lang="yaml")

            country_name = obj.name
            image = self.image_base.format(obj.alpha_2.lower())


        embed = discord.Embed(
            title=f"{emoji}: {country_name}",
            description=description,
            color=await ctx.embed_colour(),
            timestamp=datetime.datetime.now()
        )
        embed.set_image(url=image)
        await ctx.send(embed=embed)