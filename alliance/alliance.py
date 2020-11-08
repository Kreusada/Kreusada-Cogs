import discord
from validator_collection import validators
from redbot.core import commands, checks, Config
from .allianceembed import Embed

class Alliance(commands.Cog):
    """Tools for your alliance on MCOC."""

    @commands.command()
    async def timezone(self, ctx, *, timezone: str = None):
        """
        Use this command to set your timezone on your nickname.
        For example - `Kreusada [+4]`
        """
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
      
    @commands.group()
    async def alliancealert(self, ctx): #aliases: aa, alert):
        """Alert your fellow alliance mates for movement."""
        
    @alliancealert.command(invoke_without_command=True, pass_context=True, aliases=["aa", "alert"])
    async def aqstart(self, ctx):
        """Alliance Quest has started!"""
        data = Embed.create(self, ctx, title='Alliance Quest has STARTED!')
        image = ("https://media.discordapp.net/attachments/745608075670585344/772947661421805648/aqstarted.png?width=1441&height=480")
        description = (f"<770943114645864470>")
        data.set_image(url=image)
        data.description = "{}".format(description)
        await ctx.send(embed=data)
