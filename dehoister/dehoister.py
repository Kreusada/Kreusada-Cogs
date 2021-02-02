import discord
from redbot.core import commands, Config

IDENTIFIER = 435089473534
HOIST = "!\"#$%&'()*+,-./:;<=>?@0123456789"

EXPLAIN = (
    "Dehoister is a cog which allows you to automatically change the nickname "
    "of users who have a hoisting character at the start of their username. "
    "To get started, use `{p}dehoistset toggle true`, which will enable this feature. "
    "Then, you can customize the nickname via `{p}dehoistset nickname`.\n\n"
    "When new users join the guild, their nickname will automatically be changed "
    "to this configured nickname, if they have a hoisted character at the start of their name. "
    "If your bot doesn't have permissions, **this process will be cancelled**, so make sure that "
    "your bot has access to nickname changing."
)

class Dehoister(commands.Cog):
    """
    Dehoist usernames that start with hoisting characters.
    """

    __author__ = "Kreusada"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, IDENTIFIER, force_registration=True)
        self.config.register_guild(
            nickname="Ze Dehoisted",
            toggled=False
        )

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        return f"{super().format_help_for_context(ctx)}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    @commands.admin_or_permissions(administrator=True)
    @commands.command()
    async def dehoist(self, ctx: commands.Context, member: discord.Member):
        """Manually dehoist a user."""
        try:
            await member.edit(nick=await self.config.guild(ctx.guild).nickname())
            await ctx.send(f"`{member.name}` has successfully been dehoisted.")
        except discord.Forbidden:
            await ctx.send("I am not authorized to edit nicknames.")

    @commands.admin_or_permissions(administrator=True)
    @commands.group()
    async def dehoistset(self, ctx: commands.Context):
        """Settings for Dehoister."""
        
    @dehoistset.command()
    async def explain(self, ctx: commands.Context):
        """Explain how Dehoister works."""
        if await ctx.embed_requested():
            embed = discord.Embed(description=EXPLAIN.format(p=ctx.clean_prefix), color=await ctx.embed_colour())
            await ctx.send(embed=embed)
        else:
            await ctx.send(EXPLAIN.format(p=ctx.clean_prefix))

    @dehoistset.command()
    async def toggle(self, ctx: commands.Context, true_or_false: bool):
        """Toggle the Dehoister."""
        await self.config.guild(ctx.guild).toggled.set(true_or_false)
        await ctx.send("Dehoister has been enabled.") if true_or_false is True else await ctx.send("Dehoister has been disabled.")

    @dehoistset.command()
    async def nickname(self, ctx: commands.Context, *, nickname: str):
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
        if member.name.startswith(tuple(HOIST)):
            try:
                return await member.edit(nick=await self.config.guild(guild).nickname())
            except discord.Forbidden:
                pass
