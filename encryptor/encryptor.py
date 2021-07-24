import contextlib
import random
import string

from password_strength import PasswordStats
from redbot.core import commands
from redbot.core.utils import chat_formatting as cf

from .word_list import *

GREEN_CIRCLE = "\N{LARGE GREEN CIRCLE}"
YELLOW_CIRCLE = "\N{LARGE YELLOW CIRCLE}"
ORANGE_CIRCLE = "\N{LARGE ORANGE CIRCLE}"
RED_CIRCLE = "\N{LARGE RED CIRCLE}"


class Encryptor(commands.Cog):
    """
    Create, and validify the strength of passwords.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.1.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("encryptor")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("encryptor", lambda x: self)

    @commands.group()
    async def password(self, ctx):
        """
        Create, and validify the strength of passwords.
        """
        pass

    @password.group(name="generate")
    async def password_generate(self, ctx):
        """Generate passwords."""
        pass

    @password_generate.command(name="complex")
    async def password_generate_complex(self, ctx):
        """Generate a complex password."""
        await ctx.send(
            "".join(
                random.choice(string.ascii_letters[:94]) for i in range(random.randint(20, 35))
            )
        )

    @password_generate.command(name="strong")
    async def password_generate_strong(self, ctx, delimeter: str = ""):
        """
        Generate a strong password.

        **Arguments**

        * ``<delimeter>``: The character used to seperate each random word. Defaults to "-"
        """
        d = delimeter
        rc = random.choice
        rr = random.randint
        await ctx.send(
            d.join(rc(RANDOM_WORDS).capitalize() for i in range(3)) + f"{d}{rr(1,1000)}"
        )

    @password.command(name="strength")
    async def password_strength(self, ctx, password: str):
        """Validate a passwords strength."""
        conv = PasswordStats(password)
        converter = conv.strength()
        if converter < 0.250:
            emoji = RED_CIRCLE
            text = "This is a **weak** password."
        elif converter > 0.250 and converter < 0.500:
            emoji = ORANGE_CIRCLE
            text = "This is an **okay** password."
        elif converter > 0.500 and converter < 0.750:
            emoji = YELLOW_CIRCLE
            text = "This is a **good** password!"
        else:
            emoji = GREEN_CIRCLE
            text = "This is an **excellent** password!"
        await ctx.maybe_send_embed(f"**Strength rating: {round(converter * 100)}%** {emoji}\n{cf.quote(text)}")
