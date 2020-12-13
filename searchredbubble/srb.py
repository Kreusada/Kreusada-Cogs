from redbot.core import commands
from datetime import datetime
import discord

class SearchRedbubble(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  async def redbubble(self, ctx, *, search_query):
    """Search redbubble with a simple URL."""
    querytemplate = f"https://www.redbubble.com/shop/?query={search_query.title()}"
    multipleargs = querytemplate.replace(' ', '%20')
    chfmi = "Click here for search results"
    now = datetime.now()
    strftime = now.strftime("Today at %H:%M %p")
    footer = f"{strftime}"
    hassearched = f"{ctx.author.name} searched for: **{search_query.title()}**."
    e = discord.Embed(title=":desktop:  Redbubble Search",
                      description="{}\n\n**[{}]({})**".format(hassearched, chfmi, multipleargs),
                      colour=discord.Colour.red())
    e.set_footer(text=footer)
    e.set_thumbnail(url="https://user-images.githubusercontent.com/29949873/32622388-4e7a9960-c548-11e7-9be6-adbaca0545f5.png")
    await ctx.send(embed=e)
