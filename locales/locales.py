import contextlib

import babel
import langcodes
from langcodes.tag_parser import LanguageTagError
from redbot.core import commands, i18n
from redbot.core.utils.chat_formatting import humanize_number

tick = "\N{WHITE HEAVY CHECK MARK} "
cross = "\N{CROSS MARK} "
valid = lambda t, b: tick + t if b else cross + t

##########################################################################
# This cog is hidden from the Red index, whilst its still being developed.
##########################################################################

class Locales(commands.Cog):
    """
    Get information about locales and language codes.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.0.3"

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

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("locales")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("locales", lambda x: self)

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

    @locale.command()
    async def bot(self, ctx):
        """Get your bot's locale."""
        bot_locale = await i18n.get_locale_from_guild(self.bot, ctx.guild)
        is_owner = await self.bot.is_owner(ctx.author)
        msg = f"{ctx.me.name}'s locale is {bot_locale}."
        if is_owner:
            msg += f"\nYou can change it through `{ctx.clean_prefix}set locale`."
        await ctx.send(msg)

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
