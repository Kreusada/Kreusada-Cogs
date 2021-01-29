import discord
from redbot.core import commands, Config

IDENTIFIER = 435089473534
HOIST = "!\"#$%&'()*+,-./:;<=>?@0123456789"

class Dehoister(commands.Cog):
    """Dehoist usernames that start with hoisting characters."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, IDENTIFIER, force_registration=True)
        self.config.register_guild(
            nickname="Ze Dehoisted",
            toggled=True
        )

    @commands.admin_or_has_permissions(administrator=True)
    @commands.command()
    async def dehoist(self, ctx, member: discord.Member):
        """Manually dehoist a user."""
        await member.edit(nick=await self.config.guild(ctx.guild).nickname())
        await ctx.send(f"`{member.name}` has successfully been dehoisted.")

    @commands.admin_or_has_permissions(administrator=True)
    @commands.group()
    async def dehoistset(self, ctx):
        """Settings for Dehoister."""

    @dehoistset.command()
    async def toggle(self, ctx, true_or_false: bool):
        """Toggle the Dehoister."""
        await self.config.guild(ctx.guild).toggled.set(true_or_false)
        await ctx.send("Dehoister has been enabled.") if true_or_false is True else await ctx.send("Dehoister has been disabled.")

    @dehoistset.command()
    async def nickname(self, ctx, *, nickname: str):
        """Set the nickname for dehoisted members."""
        if len(nickname) < 32:
            await self.config.guild(ctx.guild).nickname.set(nickname)
            await ctx.send(f"Dehoisted members will now have their nickname set to `{nickname}`.")
        else:
            await ctx.send(f"Discord has a limit of 32 characters for nicknames. Your chosen nickname, {nickname}, could not be set.")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        if await self.config.guild(guild).toggled() is False:
            return
        if member.bot:
            return
        if not guild:
            return
        if member.name.startswith(tuple(list(HOIST))):
            try:
                return await member.edit(nick=await self.config.guild(guild).nickname())
            except discord.Forbidden:
                pass