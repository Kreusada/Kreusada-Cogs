import io
import re

import aiohttp
import discord
from PIL import Image, ImageDraw, ImageFont
from redbot.core import commands
from redbot.core.utils.chat_formatting import bold, inline

HEX_CODE_RE = re.compile(r"#?[0-9a-fA-F]{6}\b")


class HexCodeConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> discord.Colour:
        argument = argument.lower()
        if argument == "random":
            return discord.Colour.random()
        if not HEX_CODE_RE.match(argument):
            raise commands.BadArgument(
                f"Please provide a valid hex code (e.g. `{discord.Colour.random()}`). You may also state 'random' to get a random colour."
            )
        if argument[0] == "#":
            argument = argument[1:]
        return discord.Colour(int(argument, base=16))


class Colour(commands.Cog):
    """View information about a colour."""

    __author__ = "Kreusada"
    __version__ = "1.1.1"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        return

    @staticmethod
    def generate_image(
        *, colour: discord.Colour, name: str, constrast: discord.Colour
    ) -> io.BytesIO:
        img = Image.new("RGB", (1500, 500), colour.to_rgb())
        drawer = ImageDraw.Draw(img)
        font = ImageFont.load_default(size=100)
        drawer.text((10, 0), name, fill=constrast, font=font)
        l, t, r, b = drawer.textbbox((10, 0), name, font=font)
        cimg = img.crop([l - 10, t - 10, r + 10, b + 10])

        buffer = io.BytesIO()
        cimg.save(buffer, "png")
        buffer.seek(0)
        return buffer

    @commands.command(aliases=["color"])
    async def colour(self, ctx: commands.Context, colour: HexCodeConverter):
        """View information about a colour.

        Provide a HEX code or "random".
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://www.thecolorapi.com/id?hex={str(colour)[1:]}"
            ) as request:
                data = await request.json()
        if data["name"]["exact_match_name"]:
            description = f"The provided colour is referred to as {bold(data['name']['value'])}.\n"
            description += "This is an *exact* name match."
        else:
            description = (
                f"The provided colour may be referred to as {bold(data['name']['value'])}.\n"
            )
            description += "This is not an *exact* name match, but is very similar to "
            description += (
                inline(data["name"]["closest_named_hex"])
                + ", the colour which is given this name."
            )
        embed = discord.Embed(
            title=data["name"]["value"],
            description=description,
            colour=colour,
        )

        embed.add_field(name="Hex Code", value=data["hex"]["value"])
        embed.add_field(name="RGB", value=data["rgb"]["value"])
        embed.add_field(name="HSL", value=data["hsl"]["value"])
        embed.add_field(name="HSV", value=data["hsv"]["value"])
        embed.add_field(name="CMYK", value=data["cmyk"]["value"])
        embed.add_field(name="XYZ", value=data["XYZ"]["value"])

        writing_over = "\n\nWhen writing over {name}, it is visually clearer to use {choice} text, as shown in the image below.".format(
            name=data["name"]["value"].lower(),
            choice="(white/~~black~~)"
            if str(data["contrast"]["value"]) == "#ffffff"
            else "(~~white~~/black)",
        )

        embed.add_field(name="Writing over", value=writing_over, inline=False)

        embed.set_thumbnail(url=data["image"]["bare"])
        embed.set_image(url="attachment://image.png")
        image = self.generate_image(
            colour=colour,
            name=data["name"]["value"].upper(),
            constrast=int(data["contrast"]["value"][1:], base=16),
        )

        await ctx.send(embed=embed, file=discord.File(image, filename="image.png"))
