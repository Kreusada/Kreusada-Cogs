from redbot.core import commands
from datetime import datetime
import discord

class SearchGoogle(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  async def google(self, ctx, *, search_query):
    """Search google with a simple URL."""
    querytemplate = f"https://www.google.co.uk/search?source=hp&ei=z07WX6SiGrXVgwfdpa3wAQ&q={search_query.title()}"
    multipleargs = querytemplate.replace(' ', '%20')
    chfmi = "Click here for search results"
    now = datetime.now()
    strftime = now.strftime("Today at %H:%M %p")
    footer = f"{strftime}"
    hassearched = f"{ctx.author.name} searched for: **{search_query.title()}**."
    e = discord.Embed(title=":desktop:  Google Search",
                      description="{}\n\n**[{}]({})**".format(hassearched, chfmi, multipleargs),
                      colour=discord.Colour.red())
    e.set_footer(text=footer)
    e.set_thumbnail(url="https://media.discordapp.net/attachments/769165401879478302/787742449987878972/google_icon_131222.png")
    await ctx.send(embed=e)
