from redbot.core import commands
from datetime import datetime
import discord

class SearchPinterest(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  async def pinterest(self, ctx, *, search_query):
    """Search pinterest with a simple URL."""
    querytemplate = f"https://www.pinterest.co.uk/search/pins/?q={search_query.title()}"
    multipleargs = querytemplate.replace(' ', '%20')
    chfmi = "Click here for search results"
    now = datetime.now()
    strftime = now.strftime("Today at %H:%M %p")
    footer = f"{strftime}"
    hassearched = f"{ctx.author.name} searched for: **{search_query.title()}**."
    e = discord.Embed(title=":desktop:  Pinterest Search",
                      description="{}\n\n**[{}]({})**".format(hassearched, chfmi, multipleargs),
                      colour=discord.Colour.red())
    e.set_footer(text=footer)
    e.set_thumbnail(url="https://media.discordapp.net/attachments/769165401879478302/787754393873154069/social_pinterest_icon_131227.png")
    await ctx.send(embed=e)
