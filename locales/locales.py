import contextlib

import babel
import langcodes
from langcodes.tag_parser import LanguageTagError
from redbot.core import commands, i18n
from redbot.core.utils.chat_formatting import humanize_number

tick = "\N{WHITE HEAVY CHECK MARK} "
cross = "\N{CROSS MARK} "
valid = lambda t, b: tick + t if b else cross + t


class Locales(commands.Cog):
    """
    Get information about locales and language codes.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.0.2"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def get_country_from_locale(self, ctx, lang):
        bot_locale = await i18n.get_locale_from_guild(self.bot, ctx.guild)
        x = langcodes.Language.get(lang).describe(bot_locale.split('-')[0])["language"].capitalize()
        if x.startswith("Unknown"):
            return False
        return x

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.group()
    async def locale(self, ctx):
        """Get information about locales and language codes."""
        pass

    @locale.command()
    async def isvalid(self, ctx, language_code: str):
        """See if a language code is valid."""
        with contextlib.suppress(LanguageTagError):
            code = langcodes.Language.get(language_code).is_valid()
            if code:
                return await ctx.send(valid("That is a valid language code.", True))
        await ctx.send(valid("That is not a valid language code.", False))

    @locale.command()
    async def get(self, ctx, language_code: str):
        """Get the language from a language code."""
        bot_locale = await i18n.get_locale_from_guild(self.bot, ctx.guild)
        with contextlib.suppress(LanguageTagError):
            lang = langcodes.Language.get(language_code).display_name(bot_locale)
            if not lang.startswith("Unknown language"):
                return await ctx.send(lang.capitalize())
        await ctx.send("Unknown language code.")

    @commands.is_owner()
    @locale.command()
    async def bot(self, ctx):
        """Get your bot's locale."""
        bot_locale = await i18n.get_locale_from_guild(self.bot, ctx.guild)
        await ctx.send(
            f"Your bot's locale is {bot_locale}.\n"
            f"You can change it through `{ctx.clean_prefix}set locale`."
        )

    @commands.is_owner()
    @locale.command(name="set")
    async def _set(self, ctx, language_code: str):
        """Set your bot's locale."""
        await ctx.invoke(self.bot.get_command("set locale"), language_code)

    @locale.command(usage="<language_code> [writing_or_speaking]")
    async def populous(self, ctx, language_code: str, writing_or_speaking: str = "speaking"):
        """Get the number of speakers/writers for a language."""
        language_code = language_code.split('-')[0]
        with contextlib.suppress(LanguageTagError):
            if not writing_or_speaking.lower()[0] in ["s", "w"]:
                return await ctx.send(f"Please specify 'writing' or 'speaking', not '{writing_or_speaking}''.")
            country_name = await self.get_country_from_locale(ctx, language_code)
            if not country_name:
                return await ctx.send(valid("That is not a valid language code.", False))
            speaking = langcodes.Language.get(language_code).speaking_population()
            writing = langcodes.Language.get(language_code).writing_population()
            text = "Over {} people {} {}."
            if writing_or_speaking.startswith("s"):
                data = humanize_number(speaking)
                grammar = "speak"
            else:
                data = humanize_number(writing)
                grammar = "write in"
            return await ctx.send(text.format(data, grammar, country_name))
        await ctx.send(f"Unrecognized language code: '{language_code}'.")
