import contextlib

import discord
from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import pagify, box
from tabulate import tabulate


class RoleBoards(commands.Cog):
    """
    Get 'leaderboards' about guild roles, such as the users with the most roles,
    the roles with the most users, and a full list of all the roles.
    """

    __author__ = ["Kreusada"]
    __version__ = "2.0.1"

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

    @roleboard.command()
    async def listroles(self, ctx: commands.Context):
        """List all roles in this guild."""
        data = []
        description = f"Roles for {ctx.guild.name}"
        for r in sorted(list(ctx.guild.roles), key=lambda x: x.position, reverse=True):
            if r.name == "@everyone":
                continue
            name = r.name[:10] + "..." if len(r.name) > 13 else r.name
            data.append([name, str(r.id), f"{r.color} (0x{str(r.color).strip('#')})"])
        kwargs = {
            "tabular_data": data,
            "tablefmt": "simple",
            "headers": ["Role Name", "Role ID", "Color"],
        }
        data = tabulate(**kwargs)
        for page in pagify(data, page_length=1990):
            await ctx.send(box(page, lang="cs"))

    @roleboard.command()
    async def topusers(self, ctx, index: int = 20):
        """Get the users with the most roles."""
        g = ctx.guild
        data = self.get_users(g, index)
        message = "\n".join(f"#{self.td(c)} [{self.td(v[1])}] {v[0]}" for c, v in enumerate(data, 1))
        for page in pagify(message, page_length=1990):
            await ctx.send(box(message, lang="css"))

    @roleboard.command()
    async def toproles(self, ctx, index: int = 20):
        """Get the roles with the most users."""
        g = ctx.guild
        data = self.get_roles(g, index)
        message = "\n".join(f"#{self.td(c)} [{self.td(v[1])}] {v[0]}" for c, v in enumerate(data, 1))
        for page in pagify(message, page_length=1990):
            await ctx.send(box(message, lang="css"))

    @staticmethod
    def get_users(guild: discord.Guild, index: int):
        key = lambda x: len(x.roles)
        top_members = sorted([x for x in guild.members], key=key, reverse=True)
        return [(x.display_name, len(x.roles) - 1) for x in top_members[:index]]

    @staticmethod
    def get_roles(guild: discord.Guild, index: int):
        key = lambda x: len(x.members)
        top_roles = sorted([r for r in guild.roles], key=key, reverse=True)[1:]
        return [(x.name, len(x.members)) for x in top_roles[:index]]

    @staticmethod
    def td(item):
        return f"0{item}" if len(str(item)) == 1 else item
