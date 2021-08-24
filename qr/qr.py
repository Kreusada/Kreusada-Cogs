import asyncio
import contextlib
import io
import json
import operator
import pathlib
import random
from typing import Literal

import discord
import qrcode
from qrcode.exceptions import DataOverflowError
from qrcode.image import styledpil, styles
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import humanize_list
from redbot.core.utils.predicates import MessagePredicate

DEFAULT_OPENING_MESSAGE = """
Your message "{0}" will be converted into a QR code, but first you can customize
how your QR code looks. Customization does **not** prevent QR codes from working
as intended.

Would you rather be able to change the colours, or the pattern of your QR code?
You can also go with option 3 if you want the default QR code style.

`1:` Colour Focused
`2:` Pattern Focused
`3:` Skip to default

**Send your message as the corresponding number**
""".strip()

DEFAULT_DRAWER_MESSAGE = """
Please provide a number from 1 to 6 based on the style you'd like.
If you want the 'classic' QR code style, `1` is the option you'd want to go for.

Fear not, none of these styles will prevent the QR code from working.

`1:` Squares (most common)
`2:` Gapped Squares
`3:` Circled
`4:` Rounded
`5:` Vertical bars
`6:` Horizontal bars

**Send your message as the corresponding number**
""".strip()

DEFAULT_MASK_MESSAGE = """
Please also provide a number from 1 to 5 based on the color mask you'd like.
If you want the 'classic' QR code style, `1` is the option you'd want to go for.

`1:` Solid black fill (most common)
`2:` Radial Gradient
`3:` Square Gradient
`4:` Horizontal Gradient
`5:` Vertical Gradient

**Send your message as the corresponding number**
""".strip()

DEFAULT_COLOR_MESSAGE_HEADER = "Please provide a **{0}** colour.\n"
DEFAULT_COLOR_MESSAGE = (
    lambda: f"""
This should be provided as a hex code.

Make sure this colour is differentiable. Refrain from using colours
that would prevent the QR code from working reliably.

**Examples**

- `{discord.Colour(random.randint(0x000000, 0xFFFFFF))}`
- `{discord.Colour(random.randint(0x000000, 0xFFFFFF))}`

**Send your message as the corresponding number**
""".strip()
)

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class ColourConverter(commands.ColourConverter):
    async def convert(self, ctx, argument: str):
        extra_map = {"black": 0, "white": 16777215}
        try:
            original_arg = await super().convert(ctx, argument)
        except commands.BadColourArgument:
            for key, value in extra_map.items():
                if argument.lower() == key:
                    return discord.Colour(value)

            raise

        else:
            return original_arg


class QR(commands.Cog):
    """Generate a QR code."""

    __author__ = ["Kreusada"]
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot: Red = bot
        self.styles = {
            "drawers": {
                1: styles.moduledrawers.SquareModuleDrawer(),
                2: styles.moduledrawers.GappedSquareModuleDrawer(),
                3: styles.moduledrawers.CircleModuleDrawer(),
                4: styles.moduledrawers.RoundedModuleDrawer(),
                5: styles.moduledrawers.VerticalBarsDrawer(),
                6: styles.moduledrawers.HorizontalBarsDrawer(),
            },
            "masks": {
                1: styles.colormasks.SolidFillColorMask(),
                2: styles.colormasks.RadialGradiantColorMask(),
                3: styles.colormasks.SquareGradiantColorMask(),
                4: styles.colormasks.HorizontalGradiantColorMask(),
                5: styles.colormasks.VerticalGradiantColorMask(),
            },
        }
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value(self.__class__.__name__.lower(), lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = humanize_list(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    def cog_unload(self):
        with contextlib.suppress(KeyError):
            self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    async def convert_colour(
        self, ctx: commands.Context, content: str, default: Literal["black", "white"]
    ):
        default_mapping = {"white": 16777215, "black": 0}
        colour_converter = ColourConverter()
        has_sent = False
        try:
            color = await colour_converter.convert(ctx, content)
        except commands.BadArgument:
            await ctx.send(
                f'Failed to identify a colour from "{content}". The default fill colour ({default}) will be used instead.'
            )
            color = discord.Colour(default_mapping[default])
            has_sent = True
        finally:
            return color, has_sent

    async def get_colour_data(
        self, ctx, setup_message: discord.Message, shade: Literal["background", "fill"]
    ):
        check = lambda x: all(
            operator.eq(getattr(ctx, y), getattr(x, y)) for y in ("author", "channel")
        )
        message = DEFAULT_COLOR_MESSAGE_HEADER.format(shade) + DEFAULT_COLOR_MESSAGE()

        try:
            await setup_message.edit(content=message)
        except discord.NotFound:
            await ctx.send(message)
        try:
            message = await self.bot.wait_for("message", check=check, timeout=100)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond, please start over.")
            return False
        else:
            default_mapping = {"background": "white", "fill": "black"}
            color, has_sent = await self.convert_colour(
                ctx, message.content, default=default_mapping[shade]
            )
            if not has_sent:
                message = f"{shade.capitalize()} set to {color}."
                if shade == "background":
                    message += " Please provide a fill colour."
                await ctx.send(message)

            return {f"{shade[:4]}_color": color.to_rgb()}

    async def get_style_data(
        self, ctx, setup_message: discord.Message, style_type: Literal["drawers", "masks"]
    ):
        mapper = {
            "drawers": {
                "message": DEFAULT_DRAWER_MESSAGE,
                "kwarg_key": "module_drawer",
            },
            "masks": {"message": DEFAULT_MASK_MESSAGE, "kwarg_key": "color_mask"},
        }
        pred = lambda x: MessagePredicate.contained_in(list(map(str, range(1, x + 1))))
        try:
            await setup_message.edit(content=mapper[style_type]["message"])
        except discord.NotFound:
            await ctx.send(mapper[style_type]["message"])
        try:
            check = pred(len(self.styles[style_type]))
            message = await self.bot.wait_for("message", check=check, timeout=100)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond, please start over.")
            return False
        else:
            return {mapper[style_type]["kwarg_key"]: self.styles[style_type][int(message.content)]}

    @commands.command()
    async def qr(self, ctx: commands.Context, *, text: str):
        """Create a QR code from text.

        When you scan this QR code, it will take you to google with the text query,
        or the website if you provide a website. That's essentially how QR codes work.
        """
        if len(text) > 250:
            await ctx.send("Please provide a sensible number of characters.")
            return

        qrc = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
        qrc.add_data(text)

        pred = lambda x: MessagePredicate.contained_in(list(map(str, range(1, x + 1))))
        setup_message: discord.Message = await ctx.send(DEFAULT_OPENING_MESSAGE.format(text))

        try:
            result = await self.bot.wait_for("message", check=pred(3), timeout=100)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond, please start over.")
            return
        else:
            result = int(result.content)
            qrc_kwargs = {}
            embed_kwargs = {"color": 16777215}

            if result == 1:
                for shade in ("background", "fill"):
                    update = await self.get_colour_data(ctx, setup_message, shade)
                    if shade == "background":
                        embed_kwargs["color"] = discord.Colour.from_rgb(*update["back_color"])
                    if update is False:
                        return
                    qrc_kwargs.update(update)

            if result == 2:
                qrc_kwargs["image_factory"] = styledpil.StyledPilImage
                for style_type in ("drawers", "masks"):
                    update = await self.get_style_data(ctx, setup_message, style_type)
                    if update is False:
                        return
                    qrc_kwargs.update(update)

        try:
            await setup_message.edit(content="Generating QR code...")
        except discord.NotFound:
            setup_message = await ctx.send(content="Generating QR code...")

        await ctx.trigger_typing()
        # Increase time between message deletion and
        # embed sending for clarity
        await asyncio.sleep(1)
        sender_kwargs = {}

        try:
            qrc = qrc.make_image(**qrc_kwargs)
        except DataOverflowError:
            sender_kwargs["content"] = "Failed to create a QR code for this text."
        else:
            buff = io.BytesIO()
            qrc.save(buff, "png")
            buff.seek(0)
            embed = discord.Embed(**embed_kwargs)
            embed.set_image(url="attachment://qr.png")
            embed.set_author(name="Generated QR code")
            embed.add_field(name="Content", value=text)
            sender_kwargs["embed"] = embed
            sender_kwargs["file"] = discord.File(buff, filename="qr.png")
        finally:
            try:
                await setup_message.edit(**sender_kwargs)
            except (discord.HTTPException, TypeError):
                # TypeError raised because of nonjsonserializable discord.File object
                await ctx.send(**sender_kwargs)
