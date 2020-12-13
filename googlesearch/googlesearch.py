from redbot.core import commands
import discord

class GoogleSearch(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  async def google(self, ctx, *, search_query):
    """Search google with a simple URL."""
    querytemplate = f"https://www.google.co.uk/search?source=hp&ei=z07WX6SiGrXVgwfdpa3wAQ&q={search_query.title()}"
    multipleargs = querytemplate.replace(' ', '%20')
    chfmi = "Click here for search results"
    footer = f"Search google by using: {ctx.clean_prefix}google <search_query>"
    hassearched = f"{ctx.author.name} searched for... **{search_query.title()}**."
    e = discord.Embed(title="<:google:787733816566349835>  Google Search",
                      description="{}\n\n**[{}]({})**".format(hassearched, chfmi, multipleargs),
                      colour=discord.Colour.red())
    #e.set_footer(text=footer)
    await ctx.send(embed=e)
