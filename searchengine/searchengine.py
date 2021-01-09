from redbot.core import commands
from datetime import datetime
import discord

class SearchEngine(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot

  async def red_delete_data_for_user(self, **kwargs):
      """
      Nothing to delete
      """
      return
    
  @commands.group()
  async def search(self, ctx):
    """Search websites."""
    pass
    
  @search.command()
  async def google(self, ctx, *, search_query):
    """Search google with a simple URL."""
    querytemplate = f"https://www.google.co.uk/search?source=hp&ei=z07WX6SiGrXVgwfdpa3wAQ&q={search_query.capitalize()}"
    multipleargs = querytemplate.replace(' ', '%20')
    chfmi = "Click here for search results"
    now = datetime.now()
    strftime = now.strftime("Today at %H:%M %p")
    footer = f"{strftime}"
    hassearched = f"{ctx.author.name} searched for: **{search_query}**."
    e = discord.Embed(title=":desktop:  Google Search",
                      description="{}\n\n**[{}]({})**".format(hassearched, chfmi, multipleargs),
                      colour=discord.Colour.red())
    e.set_footer(text=footer)
    e.set_thumbnail(url="https://media.discordapp.net/attachments/769165401879478302/787742449987878972/google_icon_131222.png")
    await ctx.send(embed=e)

  @search.command()
  async def pinterest(self, ctx, *, search_query):
    """Search pinterest with a simple URL."""
    querytemplate = f"https://www.pinterest.co.uk/search/pins/?q={search_query.capitalize()}"
    multipleargs = querytemplate.replace(' ', '%20')
    chfmi = "Click here for search results"
    now = datetime.now()
    strftime = now.strftime("Today at %H:%M %p")
    footer = f"{strftime}"
    hassearched = f"{ctx.author.name} searched for: **{search_query}**."
    e = discord.Embed(title=":desktop:  Pinterest Search",
                      description="{}\n\n**[{}]({})**".format(hassearched, chfmi, multipleargs),
                      colour=discord.Colour.red())
    e.set_footer(text=footer)
    e.set_thumbnail(url="https://media.discordapp.net/attachments/769165401879478302/787754393873154069/social_pinterest_icon_131227.png")
    await ctx.send(embed=e)

  @search.command()
  async def redbubble(self, ctx, *, search_query):
    """Search redbubble with a simple URL."""
    querytemplate = f"https://www.redbubble.com/shop/?query={search_query.capitalize()}"
    multipleargs = querytemplate.replace(' ', '%20')
    chfmi = "Click here for search results"
    now = datetime.now()
    strftime = now.strftime("Today at %H:%M %p")
    footer = f"{strftime}"
    hassearched = f"{ctx.author.name} searched for: **{search_query}**."
    e = discord.Embed(title=":desktop:  Redbubble Search",
                      description="{}\n\n**[{}]({})**".format(hassearched, chfmi, multipleargs),
                      colour=discord.Colour.red())
    e.set_footer(text=footer)
    e.set_thumbnail(url="https://user-images.githubusercontent.com/29949873/32622388-4e7a9960-c548-11e7-9be6-adbaca0545f5.png")
    await ctx.send(embed=e)


