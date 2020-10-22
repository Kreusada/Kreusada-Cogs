from redbot.core import commands, Config, modlog
from redbot.core import checks
import discord
from .mdtembed import Embed

class get(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 13814755994)
        self.config.register_guild(
            roles={}
        )
        self.embed = Embed(self)

    @commands.group()
    async def get(self, ctx):
        """Get self assignable roles."""

    @getrole.command(name="add")
    @checks.admin()
    async def _add(self, ctx, role: discord.Role):
        """Add a purchasable role"""
        await self.config.guild(ctx.guild).roles.set_raw(role)
        data = Embed.create(self, ctx, title='**Menu: Adding Roles**')
        description = ("That role can now be self-assigned by members.")
        await ctx.send(embed=data)        

    @getrole.command(aliases=["del", ])
    @checks.admin()
    async def remove(self, ctx, *, role):
        try:
            await self.config.guild(ctx.guild).roles.clear_raw(role)
            await ctx.send("Removed that role from the store")
        except KeyError:
            await ctx.send("I couldn't find that role")

    @getrole.command()
    async def role(self, ctx, *, role: discord.Role):
        """Buy a role with credits"""
        try:
            role_cost = await self.config.guild(ctx.guild).roles.get_raw(role)
        except KeyError:
            return await ctx.send("I could not find that role!")

        if await bank.can_spend(ctx.author, role_cost):
            try:
                await ctx.author.add_roles(role)
                await bank.withdraw_credits(ctx.author, role_cost)
                await ctx.send("You have sucessfully bought that role!")
            except discord.Forbidden:
                await ctx.send("I could not attach that role!")
