from redbot.core.commands import BadArgument, Context, Converter
from redbot.core.utils.chat_formatting import box

from .alphabet import NATO_ALPHABET


class AlphaConverter(Converter):
    async def convert(self, ctx: Context, argument: str):
        argument = argument.replace(" ", "").replace(",", "")
        if not argument.isalpha():
            raise BadArgument("Please only use alphabetic characters.")

        alpha = {a[0].lower(): a for a in NATO_ALPHABET}
        if argument.lower() == "all":
            return box("\n".join(f"'{k}' = {v}" for k, v in alpha.items()), lang="ml")
        return box("\n".join(f"'{a}' = {alpha[a.lower()]}" for a in argument), lang="ml")
