import discord
from redbot.core import commands, Config
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("Edition", __file__)

@cog_i18n(_)
class Edition(commands.Cog):
    """
    Set your nickname as an edition of someone!
    Inspired by the Twentysix Edition at Red.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.1.0"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 43958345, force_registration=True)
        self.config.register_guild(editioner=None)

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        return f"{super().format_help_for_context(ctx)}\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    @commands.command()
    async def edition(self, ctx: commands.Context, type: str):
        """
        Become an edition of the editioner!
        
        Server owner nicknames cannot be changed.

        **Arguments**
        `Type`: The custom name from your input.

        **Nickname Edit Format**
        `Editioner - Type Edition`
        
        **What is Editioner?**
        `Editioner`: The name of the editioner set using `[p]editionset`.
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
                await ctx.send("I don't have permission to change your nickname. Please note that I cannot change server owner nicknames.")
            except discord.HTTPException:
                await ctx.send("Your new nickname exceeds the 32 character limit.")


    @commands.command()
    @commands.mod_or_permissions(administrator=True)
    async def editionset(self, ctx: commands.Context, editioner: discord.Member):
        """Sets the editioner."""
        await self.config.guild(ctx.guild).editioner.set(editioner.id)
        await ctx.send(f"Okay, {editioner.name} is now the guild's editioner.")
