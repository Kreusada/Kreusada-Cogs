import sys
from typing import Dict, Union

import pycountry
from redbot.core.commands import BadArgument, Context, Converter
from redbot.core.utils.chat_formatting import box

from .functions import EXCEPTIONS, IMAGE_BASE, square


class CountryConverter(Converter):
    """Convert for country input"""

    async def convert(
        self, ctx: Context, argument: str
    ) -> Union[Dict[str, Union[str, int]], None]:
        argument = argument.lower()
        get = lambda **kwargs: pycountry.countries.get(**kwargs)

        if argument in ("england", "scotland", "wales"):

            special_images = {"england": "gb-eng", "wales": "gb-wls", "scotland": "gb-sct"}

            if sys.modules.get("tabulate", None) is not None:
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
                "image": image,
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
                "image": IMAGE_BASE.format(obj.alpha_2.lower()),
            }

            for attr in ("alpha_2", "alpha_3", "numeric", "official_name"):
                if hasattr(obj, attr):
                    ret[attr] = square(getattr(obj, attr))

            return ret
