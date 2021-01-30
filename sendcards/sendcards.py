import discord
import asyncio
from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("SendCards", __file__)

@cog_i18n(_)
class SendCards(commands.Cog):
    """
    Send someone a card!
    """

    __author__ = "Kreusada"
    __version__ = "1.2.0"
  
    def __init__(self, bot):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        """Thanks Sinbad."""
        return f"{super().format_help_for_context(ctx)}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return
        
    @commands.group()
    async def send(self, ctx: commands.Context):
        """Send a card to someone!"""
      
    @send.command()
    async def christmas(self, ctx: commands.Context, user_id: int, *, message: str):
        """Send a christmas card to someone!"""
        await self.card_send(ctx, 'christmas', user_id, message)

    @send.command()
    async def birthday(self, ctx: commands.Context, user_id: int, *, message: str):
        """Send a birthday card to someone!"""
        await self.card_send(ctx, 'birthday', user_id, message)

    @send.command(aliases=["gws"])
    async def getwellsoon(self, ctx: commands.Context, user_id: int, *, message: str):
      """Send a get well soon card to someone!"""
      await self.card_send(ctx, 'get well soon', user_id, message)

    @send.command()
    async def valentine(self, ctx: commands.Context, user_id: int, *, message: str):
        """Send a valentines card to someone!"""
        await self.card_send(ctx, 'valentines', user_id, message)

    async def card_send(self, ctx: commands.Context, type: str, user_id: int, message: str):
        if len(message) > 1900:
            return await ctx.send("This message is *too* long. Please try again.")
        if type == 'christmas':
            emoji = "\N{CHRISTMAS TREE}"
        elif type == 'birthday':
            emoji = "\N{PARTY POPPER}"
        elif type == 'get well soon':
            emoji = "\N{THERMOMETER}\N{VARIATION SELECTOR-16}"
        else:
            emoji = "\N{SMILING FACE WITH SMILING EYES AND THREE HEARTS}"
        name = self.bot.get_user(user_id)
        embed = discord.Embed(
          title=f"{emoji} {type.title()} card from {ctx.author.name}!",
          description=f"Dear {name.name},\n\n{message}\n\nFrom {ctx.author.name} {emoji}.",
          color=await ctx.embed_colour()
        )
        embed.set_footer(text=f"Send {type} cards by using: {ctx.clean_prefix}send {type.replace(' ', '')}!")
        try:
            await name.send(embed=embed)
            return await ctx.send(f"A {type.capitalize()} card has been successfully sent to {name.name}! {emoji}")
        except discord.Forbidden:
            return await ctx.send(f"Unfortunately, {name.name} has their DMs turned off. Sorry!")

