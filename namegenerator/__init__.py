import contextlib
import random

import discord
import mimesis
from mimesis.enums import Gender
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils import get_end_user_data_statement

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)


LANGUAGES = {
    "ar-dz": {"name": "Arabic (Algeria)", "latin": False, "emoji": "🇩🇿"},
    "ar-eg": {"name": "Arabic (Egypt)", "latin": False, "emoji": "🇪🇬"},
    "ar-jo": {"name": "Arabic (Jordan)", "latin": False, "emoji": "🇯🇴"},
    #   "ar-kw": {"name": "Arabic (Kuwait)", "latin": False, "emoji": "🇰🇼"},
    #   "ar-ma": {"name": "Arabic (Morocco)", "latin": False, "emoji": "🇲🇦"},
    "ar-om": {"name": "Arabic (Oman)", "latin": False, "emoji": "🇴🇲"},
    #   "ar-qa": {"name": "Arabic (Qatar)", "latin": False, "emoji": "🇶🇦"},
    #   "ar-sa": {"name": "Arabic (Saudi Arabia)", "latin": False, "emoji": "🇸🇦"},
    "ar-sy": {"name": "Arabic (Syria)", "latin": False, "emoji": "🇸🇾"},
    #   "ar-tn": {"name": "Arabic (Tunisia)", "latin": False, "emoji": "🇹🇳"},
    "ar-ae": {"name": "Arabic (U.A.E)", "latin": False, "emoji": "🇦🇪"},
    "ar-ye": {"name": "Arabic (Yemen)", "latin": False, "emoji": "🇾🇪"},
    "en-au": {"name": "Australian English", "latin": True, "emoji": "🇦🇺"},
    "de-at": {"name": "Austrian German", "latin": True, "emoji": "🇦🇹"},
    "nl-be": {"name": "Belgium Dutch", "latin": True, "emoji": "🇧🇪"},
    "pt-br": {"name": "Brazilian Portuguese", "latin": True, "emoji": "🇧🇷"},
    "en-gb": {"name": "British English", "latin": True, "emoji": "🇬🇧"},
    "en-ca": {"name": "Canadian English", "latin": True, "emoji": "🇨🇦"},
    "zh": {"name": "Chinese", "latin": False, "emoji": "🇨🇳"},
    "hr": {"name": "Croatian", "latin": True, "emoji": "🇭🇷"},
    "cs": {"name": "Czech", "latin": True, "emoji": "🇨🇿"},
    "da": {"name": "Danish", "latin": True, "emoji": "🇩🇰"},
    "nl": {"name": "Dutch", "latin": True, "emoji": "🇳🇱"},
    "en": {"name": "English", "latin": True, "emoji": "🇺🇸"},
    "et": {"name": "Estonian", "latin": True, "emoji": "🇪🇪"},
    "fa": {"name": "Farsi", "latin": False, "emoji": "🇮🇷"},
    "fi": {"name": "Finnish", "latin": True, "emoji": "🇫🇮"},
    "fr": {"name": "French", "latin": True, "emoji": "🇫🇷"},
    "de": {"name": "German", "latin": True, "emoji": "🇩🇪"},
    "el": {"name": "Greek", "latin": False, "emoji": "🇬🇷"},
    "hu": {"name": "Hungarian", "latin": True, "emoji": "🇭🇺"},
    "is": {"name": "Icelandic", "latin": True, "emoji": "🇮🇸"},
    "it": {"name": "Italian", "latin": True, "emoji": "🇮🇹"},
    "ja": {"name": "Japanese", "latin": False, "emoji": "🇯🇵"},
    "kk": {"name": "Kazakh", "latin": False, "emoji": "🇰🇿"},
    "ko": {"name": "Korean", "latin": False, "emoji": "🇰🇷"},
    "es-mx": {"name": "Mexican Spanish", "latin": True, "emoji": "🇲🇽"},
    "no": {"name": "Norwegian", "latin": True, "emoji": "🇳🇴"},
    "pl": {"name": "Polish", "latin": True, "emoji": "🇵🇱"},
    "pt": {"name": "Portuguese", "latin": True, "emoji": "🇵🇹"},
    "ru": {"name": "Russian", "latin": False, "emoji": "🇷🇺"},
    "sk": {"name": "Slovak", "latin": True, "emoji": "🇸🇰"},
    "es": {"name": "Spanish", "latin": True, "emoji": "🇪🇸"},
    "sv": {"name": "Swedish", "latin": True, "emoji": "🇸🇪"},
    "de-ch": {"name": "Swiss German", "latin": True, "emoji": "🇨🇭"},
    "tr": {"name": "Turkish", "latin": True, "emoji": "🇹🇷"},
    "uk": {"name": "Ukrainian", "latin": False, "emoji": "🇺🇦"},
}

COLOURS = {
    Gender.MALE: discord.Colour.blue(),
    Gender.FEMALE: discord.Colour.pink(),
    None: discord.Colour.light_grey(),
}


def generate_name(interaction: discord.Interaction, view: "LocaleView"):
    language = view.language
    data = LANGUAGES[language]
    person = mimesis.Person(language)
    text = f"{data['emoji']} {person.full_name(gender=view.gender or (rc := random.choice([Gender.MALE, Gender.FEMALE])))}"
    if not view.gender:
        text += f" ({rc.name.lower()})"
    view.language = language
    view.text = text
    return interaction


class LocaleView(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__()
        self.ctx = ctx
        self.message: discord.Message
        self.add_item(RegenerateButton())
        self.add_item(LocaleSelect(page=1))
        self.add_item(LocaleSelect(page=2))
        self.add_item(GenderSelect())

        self.gender: Gender | None = None
        self.colour: discord.Colour = COLOURS[None]
        self.language: str | None = None
        self.text: str | None = None

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        with contextlib.suppress(discord.NotFound):
            await self.message.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                "You are not allowed to interact with this.", ephemeral=True
            )
        else:
            return True

    async def edit_message(self, interaction: discord.Interaction):
        embed = discord.Embed(
            description="# " + (self.text or "Please select a language"), colour=self.colour
        ).set_footer(
            text=f"Gender: {self.gender.name.capitalize() if self.gender else 'Either'}\nLanguage: {LANGUAGES[self.language]['name'] if self.language else None}"
        )
        await interaction.response.edit_message(view=self, embed=embed)


class RegenerateButton(discord.ui.Button):
    def __init__(self):
        self.view: LocaleView
        super().__init__(
            style=discord.ButtonStyle.green, label="Regenerate", emoji="🔁", row=0, disabled=True
        )

    async def callback(self, interaction: discord.Interaction):
        if not self.view.text:
            return await interaction.response.send_message(
                "Cannot use the redo button without a selected language.", ephemeral=True
            )
        await self.view.edit_message(interaction=generate_name(interaction, self.view))


class LocaleSelect(discord.ui.Select):
    def __init__(self, *, page: int):
        self.view: LocaleView
        languages = [
            discord.SelectOption(label=data["name"], value=code, emoji=data["emoji"])
            for code, data in LANGUAGES.items()
        ][25 * (page - 1) : 25 * page]

        super().__init__(
            placeholder=f"[{page}/2] Choose a language ({languages[0].label[0]}-{languages[-1].label[0]})",
            min_values=1,
            max_values=1,
            options=languages,
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.language = self.values[0]
        self.view.children[0].disabled = False
        await self.view.edit_message(interaction=generate_name(interaction, self.view))


class GenderSelect(discord.ui.Select):
    def __init__(self):
        self.view: LocaleView
        super().__init__(
            placeholder="Select a gender...",
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(label="Male", value="MALE", emoji="♂️"),
                discord.SelectOption(label="Female", value="FEMALE", emoji="♀️"),
                discord.SelectOption(label="Either", value="EITHER", emoji="🤷"),
            ],
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.gender = gender = getattr(Gender, self.values[0], None)
        self.view.colour = COLOURS[gender]
        if self.view.language:
            interaction = generate_name(interaction, self.view)
        await self.view.edit_message(interaction=interaction)


class NameGenerator(commands.Cog):
    """Generate names."""

    __author__ = "Kreusada"
    __version__ = "1.0.0"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        return

    @commands.command(aliases=["generatename", "namegenerate", "genname"])
    async def namegen(self, ctx: commands.Context):
        """Generate names."""
        embed = discord.Embed(
            description="# Please select a language", colour=discord.Colour.light_grey()
        ).set_footer(text="Gender: Either\nLanguage: None")
        view = LocaleView(ctx)
        view.message = await ctx.send(embed=embed, view=view)


async def setup(bot: Red):
    await bot.add_cog(NameGenerator())
