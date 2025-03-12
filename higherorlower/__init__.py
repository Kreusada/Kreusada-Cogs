from __future__ import annotations

import contextlib
import discord
import io
import random
import typing

from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Resampling
from redbot.core import Config, bank, commands
from redbot.core.bot import Red
from redbot.core.data_manager import bundled_data_path
from redbot.core.utils import get_end_user_data_statement

__red_end_user_data_statement__ = get_end_user_data_statement(__file__)

DEFAULT_ORDER = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k", "a"]
HigherLower = typing.Literal["higher", "lower"]


class HigherOrLowerView(discord.ui.View):
    def __init__(self):
        self.message: discord.Message | None = None
        self.direction: HigherLower | None = None
        self.timed_out: bool = False
        super().__init__(timeout=30)

    @discord.ui.button(label="Higher", style=discord.ButtonStyle.green)
    async def higher(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.direction = "higher"
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label="Lower", style=discord.ButtonStyle.red)
    async def lower(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.direction = "lower"
        self.stop()
        await interaction.response.defer()

    async def on_timeout(self):
        with contextlib.suppress(discord.HTTPException):
            await self.message.delete()


class HigherOrLowerSession:
    def __init__(
        self,
        cog: "HigherOrLower",
        *,
        size: tuple[int, int],
        table_colour: tuple[int, int, int],
        ace_high: bool,
        equal_survives: bool,
        rotated_style: bool,
    ):
        self.images: list[Image.Image] = []
        self.indexes: list[int] = []
        order = DEFAULT_ORDER if ace_high else [*DEFAULT_ORDER[1:], DEFAULT_ORDER[0]]

        image_path = bundled_data_path(cog) / "images"
        for path in random.sample(list(image_path.iterdir()), size[0] * size[1]):
            self.indexes.append(order.index(path.name.split(".")[0][1:]))
            self.images.append(Image.open(path).resize((250, 363)).convert("RGBA"))

        self.table_colour = table_colour
        self.equal_survives = equal_survives
        self.rotated_style = rotated_style
        self.size = size
        self.progress: int = 0
        self.ended: bool = False
        self.won: bool = False

        self.description = (
            f"### During this game...\n- Aces are considered **{'high (14)' if ace_high else 'low (1)'}**.\n"
            f"- Equals **{'are' if equal_survives else 'are not'}** a lifeline.\n"
            "These settings are configured by mods.\nThey are subject to change."
        )

    def create_image(self) -> discord.File:
        image = Image.new("RGBA", (250 * self.size[0], 363 * self.size[1]), self.table_colour)
        x = 0
        y = 0
        for index, img in enumerate(self.images[: self.progress + 1], 1):
            if self.rotated_style:
                img = img.rotate(
                    random.choice([-2, -1, 1, 2]), resample=Resampling.BICUBIC, expand=True
                )
            image.paste(img, (x, y), img)
            if not index % self.size[0]:
                y += 363
                x = 0
            else:
                x += 250

        if self.ended:
            image = image.convert("L")

        buffer = io.BytesIO()
        image.save(buffer, "png")
        buffer.seek(0)

        return discord.File(buffer, "hol.png")

    def create_thumbnail(self) -> discord.File:
        image = Image.new("RGBA", (500, 363), self.table_colour)

        if self.ended:
            card = self.images[self.progress].rotate(-8, resample=Resampling.BICUBIC, expand=True)
            image.paste(card, (200, 0), card)
            image.paste(card := self.images[self.progress - 1], (0, 0), card)

        else:
            image.paste(card := self.images[self.progress], (0, 0), card)
            ImageDraw.Draw(image).text(
                (300, 0), "?", fill="black", font=ImageFont.load_default(size=300)
            )

        buffer = io.BytesIO()
        image.save(buffer, "png")
        buffer.seek(0)

        return discord.File(buffer, "thumb.png")

    def evaluate(self, guess: HigherLower):
        current = self.indexes[self.progress]
        following = self.indexes[self.progress + 1]
        if current < following and guess == "higher" or current > following and guess == "lower":
            return True
        if current == following and self.equal_survives:
            return True
        return False

    def end_game(self):
        self.progress += 1
        self.ended = True

    def get_files(self, exclude_thumb: bool = False) -> list[discord.File]:
        if exclude_thumb:
            return [self.create_image()]
        return [self.create_image(), self.create_thumbnail()]

    async def start(self, ctx: commands.Context):
        embed = discord.Embed(
            title=f"Higher Or Lower?", description=self.description, colour=discord.Colour.green()
        )
        embed.set_image(url="attachment://hol.png")
        embed.set_thumbnail(url="attachment://thumb.png")
        odds = self.size[0] * self.size[1] * 14
        embed.set_footer(text=f"Winning odds: 1/{odds} ({round(1 / odds * 100, 3)}%)")

        view = HigherOrLowerView()
        view.message = message = await ctx.send(embed=embed, files=self.get_files(), view=view)

        while self.progress != self.size[0] * self.size[1] - 1:
            await view.wait()

            if view.timed_out:
                return

            if not self.evaluate(view.direction):
                embed.colour = discord.Colour.red()
                embed.set_footer(text="Unlucky, you lose.")
                self.end_game()
                return await message.edit(embed=embed, attachments=self.get_files(), view=None)

            self.progress += 1

            view = HigherOrLowerView()
            await message.edit(embed=embed, attachments=self.get_files(), view=view)

        self.won = True
        embed.set_footer(text="You won! 🎉")
        await message.edit(embed=embed, attachments=self.get_files(exclude_thumb=True), view=None)


class HigherOrLower(commands.Cog):
    """Play Higher Or Lower, win big!"""

    __author__ = "Kreusada"
    __version__ = "1.0.2"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 719988449867989142, force_registration=True)
        self.config.register_guild(
            payout=1000, ace_high=True, equal_survives=False, rotated_style=False, size=[2, 4]
        )
        self.config.register_user(table_colour=[165, 42, 42])

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        return

    @commands.command(aliases=["hol"])
    @commands.guild_only()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def higherorlower(self, ctx: commands.Context):
        """Play Higher Or Lower!"""
        table_colour = await self.config.user(ctx.author).table_colour()
        guild_config = await self.config.guild(ctx.guild).all()
        session = HigherOrLowerSession(
            self,
            size=tuple(guild_config["size"]),
            table_colour=tuple(table_colour),
            ace_high=guild_config["ace_high"],
            equal_survives=guild_config["equal_survives"],
            rotated_style=guild_config["rotated_style"],
        )
        with contextlib.suppress(discord.HTTPException):
            await session.start(ctx)
            if session.won:
                payout = guild_config["payout"]
                credit_name = await bank.get_currency_name(ctx.guild)
                await bank.deposit_credits(ctx.author, payout)
                await ctx.send(
                    f"Congratulations {ctx.author.mention}, you win {payout} {credit_name}!"
                )

    @commands.group()
    async def holset(self, ctx: commands.Context):
        """Configuration commands for Higher Or Lower."""

    @holset.command(name="tablecolour", aliases=["tablecolor"])
    async def holset_tablecolour(self, ctx: commands.Context, colour: discord.Colour):
        """Set the colour of your table used in games."""
        await self.config.user(ctx.author).table_colour.set(colour.to_rgb())
        if await ctx.embed_requested():
            await ctx.send(embed=discord.Embed(title="Table colour set!", colour=colour))
        else:
            await ctx.send("Table colour set!")

    @commands.mod()
    @commands.guild_only()
    @holset.command(name="payout")
    async def holset_payout(self, ctx: commands.Context, payout: commands.positive_int):
        """Mods only - Set the win payout for this guild."""
        await self.config.guild(ctx.guild).payout.set(payout)
        credit_name = await bank.get_currency_name(ctx.guild)
        await ctx.send(f"Payout set to {payout} {credit_name}")

    @commands.mod()
    @commands.guild_only()
    @holset.command(name="acehigh")
    async def holset_setace(self, ctx: commands.Context, ace_is_high: bool):
        """Mods only - Set whether ace is considered high (14)."""
        await self.config.guild(ctx.guild).ace_high.set(ace_is_high)
        await ctx.send(
            f"Ace will now be considered as {'high (14)' if ace_is_high else 'low (1)'}"
        )

    @commands.mod()
    @commands.guild_only()
    @holset.command(name="equalsurvives")
    async def holset_equalsurvives(self, ctx: commands.Context, survives: bool):
        """Mods only - Set whether players survive on an equal card."""
        await self.config.guild(ctx.guild).equal_survives.set(survives)
        grammar = "now" if survives else "now **not**"
        await ctx.send(f"Equal cards will {grammar} be considered a lifeline.")

    @commands.mod()
    @commands.guild_only()
    @holset.command(name="rotatedstyle")
    async def holset_rotatedstyle(self, ctx: commands.Context, use: bool):
        """Mods only - Set whether placed cards on the table use rotated style."""
        await self.config.guild(ctx.guild).rotated_style.set(use)
        grammar = "now" if use else "now **not**"
        await ctx.send(f"Placed cards will {grammar} use rotated style.")

    @commands.mod()
    @commands.guild_only()
    @holset.command(name="size")
    async def holset_size(
        self, ctx: commands.Context, x: commands.Range[int, 1, 10], y: commands.Range[int, 1, 10]
    ):
        """Mods only - Set the grid size."""
        if x * y < 4:
            return await ctx.send("Grid size is too small.")
        if x * y > 52:
            return await ctx.send("Grid size is too large.")
        await self.config.guild(ctx.guild).size.set([x, y])
        await ctx.send(f"Grid size set to {x}x{y}.")

    @commands.guild_only()
    @holset.command(name="showsettings", aliases=["settings"])
    async def holset_showsettings(self, ctx: commands.Context):
        """Mods only - See the current settings for Higher Or Lower."""
        message = f"# Higher Or Lower settings\nYour table colour: {discord.Colour.from_rgb(*(await self.config.user(ctx.author).table_colour()))}\n"
        if await self.bot.is_mod(ctx.author):
            config = await self.config.guild(ctx.guild).all()
            for key, value in config.items():
                if key == "size":
                    value = "x".join(map(str, value))
                message += f"{key.replace('_', ' ').capitalize()}: {value}\n"
        await ctx.send(message)


async def setup(bot: Red):
    await bot.add_cog(HigherOrLower(bot))
