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
    __version__ = "2.0.0"

    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        authors = ", ".join(self.__author__)
        return f"{context}\n\nAuthor: {authors}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

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
            name = r.name[:14] + "..." if len(r.name) > 17 else r.name
            data.append([name, str(r.id), f"{r.color} (0x{str(r.color).strip('#')})"])
        kwargs = {
            "tabular_data": data,
            "tablefmt": "simple",
            "headers": ["Role Name", "Role ID", "Color"],
        }
        data = tabulate(**kwargs)
        for page in pagify(data, page_length=1998):
            page = box(page, lang="cs")
            if await ctx.embed_requested():
                await ctx.send(
                    embed=discord.Embed(
                        description=page,
                        color=await ctx.embed_colour(),
                    )
                )
            else:
                await ctx.send(page)

    @roleboard.command()
    async def topusers(self, ctx):
        """Get the users with the most roles."""
        g = ctx.guild
        data = self.get_roles(g)
        await ctx.send(
            embed=discord.Embed(
                title="Users with the most roles",
                description=box(
                    "\n".join(
                        f"#{self.td(c)} [{self.td(v[1])}] {v[0]}" for c, v in enumerate(data, 1)
                    ),
                    lang="css",
                ),
                color=await ctx.embed_colour(),
            )
        )

    @roleboard.command()
    async def toproles(self, ctx):
        """Get the roles with the most users."""
        g = ctx.guild
        data = []
        for r in sorted([r for r in g.roles], key=lambda x: len(x.members), reverse=True)[:11]:
            if r.name == "@everyone":
                continue
            data.append((r.name, len(r.members)))
        await ctx.send(
            embed=discord.Embed(
                title="Roles with the most users",
                description=box(
                    "\n".join(
                        f"#{self.td(c)} [{self.td(v[1])}] {v[0]}" for c, v in enumerate(data, 1)
                    ),
                    lang="css",
                ),
                color=await ctx.embed_colour(),
            )
        )

    @staticmethod
    def get_roles(guild: discord.Guild):
        key = lambda x: len(x.roles)
        top_members = sorted([x for x in guild.members], key=key, reverse=True)
        return [(x.display_name, len(x.roles) - 1) for x in top_members[:10]]

    @staticmethod
    def td(item):
        return f"0{item}" if len(str(item)) == 1 else item