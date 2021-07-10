import contextlib
from typing import List, Literal, Tuple

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu

perms = {"embed_links": True, "add_reactions": True}


class ValidRoleIndex(commands.Converter):
    async def convert(self, ctx: commands.Context, argument):
        try:
            argument = int(argument)
        except ValueError:
            raise commands.BadArgument("Please provide an integer.")
        if argument > (len(ctx.guild.roles) - 1):
            raise commands.BadArgument(
                "Please provide an index lower than the number of roles in this guild."
            )
        return argument


class ValidUserIndex(commands.Converter):
    async def convert(self, ctx: commands.Context, argument):
        try:
            argument = int(argument)
        except ValueError:
            raise commands.BadArgument("Please provide an integer.")
        if argument > len(ctx.guild.members):
            raise commands.BadArgument(
                "Please provide an index lower than the number of users in this guild."
            )
        return argument


class RoleBoards(commands.Cog):
    """
    Get 'leaderboards' about guild roles, such as the users with the most roles,
    the roles with the most users, and a full list of all the roles.
    """

    __author__ = ["Kreusada"]
    __version__ = "3.1.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    def cog_unload(self):
        with contextlib.suppress(Exception):
            self.bot.remove_dev_env_value("roleboards")

    async def initialize(self) -> None:
        if 719988449867989142 in self.bot.owner_ids:
            with contextlib.suppress(Exception):
                self.bot.add_dev_env_value("roleboards", lambda x: self)

    @commands.group(aliases=["rb"])
    @commands.guild_only()
    async def roleboard(self, ctx):
        """Get roleboards for this server.."""
        pass

    @roleboard.command(aliases=["topusers"])
    @commands.bot_has_permissions(**perms)
    async def topmembers(self, ctx, index: ValidUserIndex):
        """Get the members with the most roles.

        \u200b
        **Arguments**

        -   ``<index>``: The number of members to get the data for.
        """
        data = self.get_users(ctx.guild, index)
        data = self.format_embed_pages(ctx, data, "members")
        await menu(ctx, await data, DEFAULT_CONTROLS)

    def get_users(self, guild: discord.Guild, index: int):
        key = lambda x: len(x.roles)
        top_members = sorted([x for x in guild.members], key=key, reverse=True)
        data = [(x.display_name, len(x.roles) - 1) for x in top_members[:index]]
        return list(self.yield_chunks(data, 10))

    @roleboard.command()
    @commands.bot_has_permissions(**perms)
    async def toproles(self, ctx, index: ValidRoleIndex):
        """Get the roles with the most members.

        \u200b
        **Arguments**

        -   ``<index>``: The number of roles to get the data for.
        """
        data = self.get_roles(ctx.guild, index)
        data = self.format_embed_pages(ctx, data, "roles")
        await menu(ctx, await data, DEFAULT_CONTROLS)

    def get_roles(self, guild: discord.Guild, index: int):
        key = lambda x: len(x.members)
        roles = []

        for r in guild.roles:
            if r.id == guild.id:
                continue
            roles.append(r)

        top_roles = sorted(roles, key=key, reverse=True)
        data = [(x.name, len(x.members)) for x in top_roles[:index]]
        return list(self.yield_chunks(data, 10))

    @staticmethod
    def yield_chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i : i + n]

    @staticmethod
    async def format_embed_pages(
        ctx: commands.Context,
        data: List[Tuple[str, int]],
        data_type: Literal["roles", "members"],
    ):
        pages = []
        enum = 1
        two_digits = lambda x: f"0{x}" if len(str(x)) == 1 else x
        reverse_types = {"roles": "members", "members": "roles"}
        total_data = len(getattr(ctx.guild, data_type))

        if data_type == "roles":
            total_data -= 1

        for sector in data:
            description = "\n".join(
                f"#{two_digits(c)} [{two_digits(v[1])}] {v[0]}" for c, v in enumerate(sector, enum)
            )
            embed = discord.Embed(
                title=f"{data_type.capitalize()} with the most {reverse_types[data_type]}",
                description=box(description, lang="css"),
                color=await ctx.embed_colour(),
            )

            embed.set_footer(text=f"Page {data.index(sector)+1}/{len(data)}")

            embed.set_author(
                name=ctx.guild.name + f" | {total_data} {data_type}", icon_url=ctx.guild.icon_url
            )

            pages.append(embed)
            enum += 10

        return pages
