from typing import Literal

import discord
import oceanscript
from oceanscript.errors import OceanScriptError, UnsupportedCharacterError
from redbot.core import commands
from redbot.core.utils.chat_formatting import box, pagify
from redbot.core.utils.embed import randomize_colour


def build_embed(codetype: Literal["encoder", "decoder"], input, output):
    embed = discord.Embed()
    embed.set_author(
        name=f"OceanScript {codetype.capitalize()}",
        url="https://github.com/Kreusada/OceanScript#readme",
    )
    embed.add_field(name="Input", value=box(input), inline=False)
    embed.add_field(name="Output", value=box(output), inline=False)
    randomize_colour(embed)
    return embed


class OceanScript(commands.Cog):
    """Encode and decode oceanscript."""

    @commands.group(aliases=["ocs"])
    async def ocean(self, ctx: commands.Context):
        """Encode and decode oceanscript."""

    @ocean.command()
    async def encode(self, ctx: commands.Context, *, text: str):
        kwargs = {}
        try:
            encoded_message = oceanscript.encode(text)
        except UnsupportedCharacterError as e:
            kwargs["content"] = str(e)
        else:
            embed = build_embed("encoder", text, encoded_message)
            kwargs["embed"] = embed
        finally:
            await ctx.send(**kwargs)

    @ocean.command()
    async def decode(self, ctx: commands.Context, *, text: str):
        kwargs = {}
        try:
            decoded_message = oceanscript.decode(text)
        except OceanScriptError as e:
            kwargs["content"] = str(e)
        else:
            embed = build_embed("decoder", text, decoded_message)
            kwargs["embed"] = embed
        finally:
            await ctx.send(**kwargs)


def setup(bot):
    bot.add_cog(OceanScript())
