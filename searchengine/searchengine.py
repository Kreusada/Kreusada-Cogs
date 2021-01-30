import discord
from datetime import datetime
from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.utils.chat_formatting import box

_ = Translator("SearchEngine", __file__)

@cog_i18n(_)
class SearchEngine(commands.Cog):
    """
    Search multiple websites for queries.
    """

    __author__ = ["Kreusada"]
    __version__ = "1.3.0"
  
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
      
    @commands.command()
    async def google(self, ctx: commands.Context, *, search_query):
        """Search google."""
        await self.boot_engine(ctx, 'google', search_query)

    @commands.command()
    async def pinterest(self, ctx: commands.Context, *, search_query):
        """Search pinterest."""
        await self.boot_engine(ctx, 'pinterest', search_query)

    @commands.command()
    async def redbubble(self, ctx: commands.Context, *, search_query):
        """Search redbubble."""
        await self.boot_engine(ctx, 'redbubble', search_query)

    async def boot_engine(self, ctx: commands.Context, type: str, search_query: str):
        if type == 'google':
            URL = f"https://www.google.co.uk/search?source=hp&ei=z07WX6SiGrXVgwfdpa3wAQ&q={search_query.capitalize()}"
        elif type == 'pinterest':
            URL = f"https://www.pinterest.co.uk/search/pins/?q={search_query.capitalize()}"
        else:
            URL = f"https://www.redbubble.com/shop/?query={search_query.capitalize()}"
        if await ctx.embed_requested():
            e = discord.Embed(
              description=(f"[Click here for search results]({URL.replace(' ', '%20')})"),
              colour=await ctx.embed_colour(), 
              timestamp=ctx.message.created_at
            )
            e.add_field(name="Engine", value=type.capitalize(), inline=True)
            e.add_field(name="Author", value=ctx.author.name, inline=True)
            e.add_field(name="Search Query", value=search_query, inline=False)
            await ctx.send(embed=e)
        else:
            title = f"URL: [{URL.replace(' ', '%20')}]"
            text = (
              f"Engine: Google\n"
              f"Author: {ctx.author.name}\n"
              f"Search Query: {search_query}"
            )
            await ctx.send(box(title, lang='ini'))
            await ctx.send(box(text, lang='yaml'))



