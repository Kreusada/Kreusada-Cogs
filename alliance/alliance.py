import discord
from validator_collection import validators
from redbot.core import commands, checks, Config

class Alliance(commands.Cog):
    """Tools for your alliance on MCOC."""

    @commands.command()
    async def timezone(self, ctx, timezone):
        if timezone is None:
            await ctx.author.edit(nick=ctx.author.name)
            return await ctx.send("Your timezone was reset. It will no longer show on your Discord nickname.")
        user = ctx.author
        before = ctx.author.name
        after = timezone
        tag = "{0} [{1}]".format(before, after)
        try:
            await user.edit(nick=tag)
        except discord.Forbidden:
            await ctx.send("Your nickname could not be changed, I don't have permission to change it. :man_shrugging:")

        await ctx.send("Your timezone was successfully added to your nickname. ``{}``".format(tag))
