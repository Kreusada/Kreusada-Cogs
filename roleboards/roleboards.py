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

    @commands.group()
    @commands.guild_only()
    async def rb(self, ctx):
        """Get roleboards for this server.."""
        pass

    @rb.command()
    async def listroles(self, ctx: commands.Context):
        """List all roles in this guild."""
        data = []
        description = f"Roles for {ctx.guild.name}"
        for r in sorted(list(ctx.guild.roles), key=lambda x: x.position, reverse=True):
            if r.name == "@everyone":
                continue
            if len(r.name) > 17:
                name = r.name[:14] + '...'
            else:
                name = r.name
            data.append([name, str(r.id), f"{r.color} (0x{str(r.color).strip('#')})"])
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

    @rb.command()
    async def topusers(self, ctx):
        """Get the users with the most roles."""
        g = ctx.guild
        data = [(x.display_name, len(x.roles) - 1) for x in sorted([x for x in g.members], key=lambda x: len(x.roles), reverse=True)[:10]]
        two_digit = lambda x: f'0{x}' if len(str(x)) == 1 else x
        td = two_digit
        await ctx.send(
            embed=discord.Embed(
                title="Users with the most roles",
                description=box("\n".join(f"#{td(c)} [{td(v[1])}] {v[0]}" for c, v in enumerate(data, 1)), lang="css"),
                color=await ctx.embed_colour(),
            )
        )

    @rb.command()
    async def toproles(self, ctx):
        """Get the roles with the most users."""
        g = ctx.guild
        data = []
        for r in sorted([r for r in g.roles], key=lambda x: len(x.members), reverse=True)[:11]:
            if r.name == "@everyone":
                continue
            data.append((r.name, len(r.members)))
        two_digit = lambda x: f'0{x}' if len(str(x)) == 1 else x
        td = two_digit
        await ctx.send(
            embed=discord.Embed(
                title="Roles with the most users",
                description=box("\n".join(f"#{td(c)} [{td(v[1])}] {v[0]}" for c, v in enumerate(data, 1)), lang="css"),
                color=await ctx.embed_colour(),
            )
        )