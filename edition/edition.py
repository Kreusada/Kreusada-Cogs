import discord
from redbot.core import commands, checks, Config

class Edition(commands.Cog):
    """
    Set your nickname as an edition of someone!
    Inspired by the Twentysix Edition at Red.
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 43958345, force_registration=True)
        self.config.register_guild(editioner=None)

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    @commands.command()
    async def edition(self, ctx, type: str):
        """
        Become an edition of the editioner!

        **Nickname Formatting Arguments**
        `Editioner`: The name of the guild's editioner.
        `Type`: The custom name from your input.

        **Nickname Edit**
        `Editioner - Type Edition`

        """
        editioner = await self.config.guild(ctx.guild).editioner()
        editioner = discord.utils.get(ctx.guild.members, id=editioner)
        if editioner is None:
            await ctx.send("You have not setup an editioner yet.")    
        else:
            try:
                await ctx.author.edit(nick=f"{editioner.name.capitalize()} - {type} Edition")
                await ctx.send(f"Done. Your nickname is now `{editioner.name.capitalize()} - {type} Edition`.")
            except discord.Forbidden:
                await ctx.send("I don't have permission to change your nickname.")


    @commands.command()
    @commands.mod_or_permissions(administrator=True)
    async def editionset(self, ctx, editioner: discord.Member):
        """Sets the editioner."""
        await self.config.guild(ctx.guild).editioner.set(editioner.id)
        await ctx.send(f"Okay, {editioner.name} is now the guild's editioner.")
