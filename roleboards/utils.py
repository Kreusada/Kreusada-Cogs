import discord

from typing import List, Literal, Tuple

from redbot.core.commands import BadArgument, Context, Converter
from redbot.core.utils.chat_formatting import box


class ValidRoleIndex(Converter):
    async def convert(self, ctx: Context, argument):
        try:
            argument = int(argument)
        except ValueError:
            raise BadArgument("Please provide an integer.")
        if argument > (len(ctx.guild.roles) - 1):
            raise BadArgument(
                "Please provide an index lower than the number of roles in this guild."
            )
        return argument


class ValidUserIndex(Converter):
    async def convert(self, ctx: Context, argument):
        try:
            argument = int(argument)
        except ValueError:
            raise BadArgument("Please provide an integer.")
        if argument > len(ctx.guild.members):
            raise BadArgument(
                "Please provide an index lower than the number of users in this guild."
            )
        return argument


def format_embed_pages(
    ctx: Context,
    *,
    data: List[Tuple[str, int]],
    data_type: Literal["roles", "members"],
    embed_colour: discord.Colour,
):
    pages = []
    enum = 1
    two_digits = lambda x: f"0{x}" if len(str(x)) == 1 else x
    reverse_types = {"roles": "members", "members": "roles"}
    total_data = len(getattr(ctx.guild, data_type))

    if data_type == "roles":
        total_data -= 1  # @everyone

    for sector in data:
        description = "\n".join(
            f"#{two_digits(c)} [{two_digits(v[1])}] {v[0]}" for c, v in enumerate(sector, enum)
        )
        embed = discord.Embed(
            title=f"{data_type.capitalize()} with the most {reverse_types[data_type]}",
            description=box(description, lang="css"),
            color=embed_colour,
        )

        embed.set_footer(text=f"Page {data.index(sector)+1}/{len(data)}")

        embed.set_author(
            name=ctx.guild.name + f" | {total_data} {data_type}", icon_url=ctx.guild.icon.url
        )

        pages.append(embed)
        enum += 10

    return pages


def yield_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def get_roles(guild: discord.Guild, *, index: int):
    key = lambda x: len(x.members)
    roles = [r for r in guild.roles if r.id != guild.id]  # exclude @everyone
    top_roles = sorted(roles, key=key, reverse=True)
    data = [(x.name, len(x.members)) for x in top_roles[:index]]
    return list(yield_chunks(data, 10))


def get_members(guild: discord.Guild, *, index: int):
    key = lambda x: len(x.roles)
    top_members = sorted([x for x in guild.members], key=key, reverse=True)
    data = [(x.display_name, len(x.roles) - 1) for x in top_members[:index]]
    return list(yield_chunks(data, 10))
