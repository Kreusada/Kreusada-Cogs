import contextlib
import io
import json
import pathlib

import aiohttp
import discord
from PIL import Image, ImageOps
from redbot.core import commands

with open(pathlib.Path(__file__).parent / "info.json") as fp:
    __red_end_user_data_statement__ = json.load(fp)["end_user_data_statement"]


class Inverter(commands.Cog):
    """Invert images."""

    def __init__(self, bot):
        self.bot = bot
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(RuntimeError, ValueError):
                self.bot.add_dev_env_value("inverter", lambda x: self)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value(self.__class__.__name__.lower())

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return

    async def invert_image(
        self,
        ctx: commands.Context,
        url,
        user: discord.Member,
        image_type: str,
    ):
        # Than
        await ctx.trigger_typing()
        if len(ctx.message.attachments) > 0:
            data = await ctx.message.attachments[0].read()
        elif url is not None:
            if url.startswith("<") and url.endswith(">"):
                url = url[1:-1]

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(url) as r:
                        data = await r.read()
                except aiohttp.InvalidURL:
                    return await ctx.send("That URL is invalid.")
                except aiohttp.ClientError:
                    return await ctx.send("Something went wrong while trying to get the image.")
        else:
            await ctx.send_help()
            return

        data = io.BytesIO(data)
        try:
            image = Image.open(data)
            image = ImageOps.invert(image.convert("RGB"))
        except Exception:
            return await ctx.send(
                "Failed to invert. Make sure that you have provided an image and in the correct format."
            )

        buff = io.BytesIO()
        image.save(buff, "png")
        buff.seek(0)
        embed = discord.Embed(
            title=f"Inverted {image_type.capitalize()}",
            color=await ctx.embed_colour(),
        )
        embed.set_image(url="attachment://image.png")
        embed.set_author(name=user.name, icon_url=user.avatar_url)
        await ctx.send(file=discord.File(buff, filename="image.png"), embed=embed)

    @commands.group(invoke_without_command=True)
    async def invert(self, ctx, url: str = None):
        """Invert an image.

        You can either upload an image or paste a URL.
        """
        msg = await ctx.send("Inverting image...")
        await self.invert_image(
            ctx=ctx,
            url=url,
            user=ctx.author,
            image_type="image",
        )
        with contextlib.suppress(discord.NotFound):
            await msg.delete()

    @invert.command()
    async def avatar(self, ctx, member: discord.Member = None):
        """Invert a user's avatar.

        If no user is provided, it defaults to yourself.
        """
        msg = await ctx.send("Inverting avatar...")
        if not member:
            member = ctx.author
        avvy = str(member.avatar_url_as(format="png"))
        await self.invert_image(
            ctx=ctx,
            url=avvy,
            user=ctx.author,
            image_type="avatar",
        )
        with contextlib.suppress(discord.NotFound):
            await msg.delete()
