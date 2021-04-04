import discord
from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import pagify, box
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS as df
from tabulate import tabulate

colon = lambda x: x + ':'
header = lambda x: x + '\n' + '=' * len(x)


class ListRoles(commands.Cog):
    """Get a list of all the roles in a server."""

    __author__ = ["Kreusada"]
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command()
    @commands.guild_only()
    async def listroles(self, ctx: commands.Context):
        """List all roles in this guild."""
        data = {}
        description = f"Roles for {ctx.guild.name}"
        for r in sorted(list(ctx.guild.roles), key=lambda x: x.position, reverse=True):
            if r.name == "@everyone":
                continue
            data[colon(r.name)] = str(r.id)
        kwargs = {
            "tabular_data": ([k, v] for k, v in data.items()),
            "tablefmt": "simple",
            "headers": ["Role Name", "Role ID"],
        }
        data = list(pagify(box(tabulate(**kwargs), lang="autohotkey")))
        title = "Roles in {}".format(ctx.guild.name)
        await ctx.send(box(header(title), lang="md"))
        await menu(ctx, data, df)