from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.views import SimpleMenu

from .utils import ValidRoleIndex, ValidUserIndex, format_embed_pages, get_members, get_roles

roleboard_perms = commands.bot_has_permissions(embed_links=True, add_reactions=True)


class RoleBoards(commands.Cog):
    """
    Get 'leaderboards' about guild roles, such as the users with the most roles
    and the roles with the most users.
    """

    __author__ = "Kreusada"
    __version__ = "3.2.1"

    def __init__(self, bot: Red):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        return

    @commands.group(aliases=["roleboards", "rb"])
    @commands.guild_only()
    async def roleboard(self, ctx: commands.Context):
        """Get roleboards for this server.."""
        pass

    @roleboard.command(aliases=["topusers"])
    @roleboard_perms
    async def topmembers(self, ctx: commands.Context, index: ValidUserIndex):
        """Get the members with the most roles.

        **Arguments**

        -   ``<index>``: The number of members to get the data for.
        """
        data = get_members(ctx.guild, index=index)
        pages = format_embed_pages(
            ctx, data=data, data_type="members", embed_colour=await ctx.embed_colour()
        )
        menu = SimpleMenu(pages, use_select_menu=True)
        await menu.start(ctx)

    @roleboard.command()
    @roleboard_perms
    async def toproles(self, ctx: commands.Context, index: ValidRoleIndex):
        """Get the roles with the most members.

        **Arguments**

        -   ``<index>``: The number of roles to get the data for.
        """
        data = get_roles(ctx.guild, index=index)
        pages = format_embed_pages(
            ctx, data=data, data_type="roles", embed_colour=await ctx.embed_colour()
        )
        menu = SimpleMenu(pages, use_select_menu=True)
        await menu.start(ctx)
