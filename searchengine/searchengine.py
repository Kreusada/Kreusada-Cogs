from redbot.core import commands
from datetime import datetime
import discord

from redbot.core import commands
from redbot.core.i18n import Translator, cog_i18n

_ = Translator("SearchEngine", __file__)

@cog_i18n(_)
class SearchEngine(commands.Cog):
  """Search multiple websites for queries."""
  
  def __init__(self, bot):
    self.bot = bot

  async def red_delete_data_for_user(self, **kwargs):
      """
      Nothing to delete
      """
      return
    
  @commands.command()
  async def google(self, ctx, *, search_query):
    """Search google."""
    querytemplate = f"https://www.google.co.uk/search?source=hp&ei=z07WX6SiGrXVgwfdpa3wAQ&q={search_query.capitalize()}"
    querytemplate = querytemplate.replace(' ', '%20')
    footer = ctx.message.created_at
    hassearched = f"{ctx.author.name} searched for: **{search_query}**."
    e = discord.Embed(description=(
      f"**Engine:** Pinterest\n"
      f"**Search query:** {search_query}\n"
      f"**Author**: {ctx.author.name}\n"
      f"**Search results:** [Click here]({querytemplate})"
    ),
    colour=discord.Colour.red(),
    timestamp=ctx.message.created_at)
    await ctx.send(embed=e)

  @commands.command()
  async def pinterest(self, ctx, *, search_query):
    """Search pinterest."""
    querytemplate = f"https://www.pinterest.co.uk/search/pins/?q={search_query.capitalize()}"
    querytemplate = querytemplate.replace(' ', '%20')
    footer = ctx.message.created_at
    hassearched = f"{ctx.author.name} searched for: **{search_query}**."
    e = discord.Embed(description=(
      f"**Engine:** Pinterest\n"
      f"**Search query:** {search_query}\n"
      f"**Author**: {ctx.author.name}\n"
      f"**Search results:** [Click here]({querytemplate})"
    ),
    colour=discord.Colour.red(),
    timestamp=ctx.message.created_at)
    await ctx.send(embed=e)

  @commands.command()
  async def redbubble(self, ctx, *, search_query):
    """Search redbubble."""
    querytemplate = f"https://www.redbubble.com/shop/?query={search_query.capitalize()}"
    querytemplate = querytemplate.replace(' ', '%20')
    footer = ctx.message.created_at
    hassearched = f"{ctx.author.name} searched for: **{search_query}**."
    e = discord.Embed(description=(
      f"**Engine:** Pinterest\n"
      f"**Search query:** {search_query}\n"
      f"**Author**: {ctx.author.name}\n"
      f"**Search results:** [Click here]({querytemplate})"
    ),
    colour=discord.Colour.red(),
    timestamp=ctx.message.created_at)
    await ctx.send(embed=e)


