"""Module for the Register cog."""
import discord
from redbot.core import commands


class SelfRole(commands.Converter):
    """Same converter as the one used in Admin, except it grabs the cog differently."""

    async def convert(self, ctx: commands.Context, arg: str) -> discord.Role:
        """Convert an arg to a SelfRole."""
        admin = ctx.bot.get_cog("Admin")
        if admin is None:
            raise commands.BadArgument("Admin is not loaded.")

        selfroles = await admin.config.guild(ctx.guild).selfroles()

        role_converter = commands.RoleConverter()
        role = await role_converter.convert(ctx, arg)

        if role.id not in selfroles:
            raise commands.BadArgument("The provided role is not a valid selfrole.")
        return role


class Register(getattr(commands, "Cog", object)):
    """Register - Simplifies two SelfRole commands into one."""

    @commands.command()
    async def register(self, ctx: commands.Context, *, role: SelfRole):
        """Register for a role.
        This command works as an alias for both `[p]selfrole` and `[p]selfrole
        remove`. Which one it aliases depends on whether or not you already have
        the requested role.
        """
        admin_cog = ctx.bot.get_cog("Admin")
        if admin_cog is None:
            await ctx.send("The `admin` cog must be loaded to use this command.")
            return

        if role in ctx.author.roles:
            cmd = admin_cog.selfrole_remove
        else:
            cmd = admin_cog.selfrole_add

        await ctx.invoke(cmd, selfrole=role)
