import contextlib
import datetime
import discord
import pycountry

try:
    import tabulate
except ModuleNotFoundError:
    tabulate = None
    
from typing import Dict, Union

from redbot.core import commands
from redbot.core.commands import BadArgument, Cog, Context, Converter
from redbot.core.utils.chat_formatting import box, humanize_list


def square(t):
    return f"[{t}]"


def format_attr(t):
    return t.replace('_',' ').title()


EXCEPTIONS = {"russia": "ru"}
IMAGE_BASE = "https://flagpedia.net/data/flags/w580/{}.png"


class Country(Converter):
    """country converter"""

    async def convert(self, ctx: Context, argument: str) -> Union[Dict[str, Union[str, int]], None]:
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
            image = IMAGE_BASE.format(special_images[argument])
            name = country_name.title()

            return {
                "description": description,
                "emoji": emoji,
                "name": square(country_name.title()),
                "title": f"{emoji} {name}",
                "image": image
            }

        else:

            obj = get(name=argument) or get(alpha_2=argument)
            if not obj:
                obj = None
                for k, v in EXCEPTIONS.items():
                    if k in argument:
                        obj = get(alpha_2=v)
                        break
                if not obj:
                    raise BadArgument("Could not match this argument to a country.")
            
            ret = {
                "name": square(obj.name.title()), 
                "title": f":flag_{obj.alpha_2.lower()}: {obj.name}",
                "emoji": square(f":flag_{obj.alpha_2.lower()}:"),
                "image": IMAGE_BASE.format(obj.alpha_2.lower())
            }

            for attr in ("alpha_2", "alpha_3", "numeric", "official_name"):
                if hasattr(obj, attr):
                    ret[attr] = square(getattr(obj, attr))
                
            return ret

class Flags(Cog):
    """Get flags from country names."""
    
    __version__ = "1.0.0"
    __author__ = ["Kreusada"]

    def __init__(self, bot):
        self.bot = bot


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
    async def flag(self, ctx: Context, *, argument: Country):
        """Get the flag for a country.
        
        Either the country name or alpha 2 code can be provided.
        
        **Examples:**

            - ``[p]flag russia``
            - ``[p]flag brazil``
            - ``[p]flag dk``
            - ``[p]flag se``
        """
        description = argument.get("description", None)
        image = argument["image"]
        title = argument["title"]

        del argument["image"]
        del argument["title"]

        if description is None:
            if tabulate:
                description = box(tabulate.tabulate([(format_attr(k), v) for k, v in argument.items()], tablefmt="plain"), lang="ini")
            else:
                description = box((f"{format_attr(k)}: {v}" for k, v in argument.items()), lang="yaml")



        embed = discord.Embed(
            title=title,
            description=description,
            color=await ctx.embed_colour(),
            timestamp=datetime.datetime.now()
        )

        embed.set_image(url=image)
        await ctx.send(embed=embed)