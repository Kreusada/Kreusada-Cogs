import discord
from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import pagify, box
from tabulate import tabulate


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
        data = []
        description = f"Roles for {ctx.guild.name}"
        for r in sorted(list(ctx.guild.roles), key=lambda x: x.position, reverse=True):
            if r.name == "@everyone":
                continue
            data.append([r.name, str(r.id), f"{r.color} (0x{str(r.color).strip('#')})"])
        kwargs = {
            "tabular_data": data,
            "tablefmt": "simple",
            "headers": ["Role Name", "Role ID", "Color"],
        }
        data = tabulate(**kwargs)
        for page in pagify(data, page_length=1998):
            if await ctx.embed_requested():
                embed = discord.Embed(
                    description=box(page, lang="cs"),
                    color=await ctx.embed_colour(),
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(box(page, lang='cs'))