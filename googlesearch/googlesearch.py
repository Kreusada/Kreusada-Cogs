from redbot.core import commands
import discord

class GoogleSearch(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  async def google(self, ctx, search_query: str):
    """Search google with a simple URL."""
    UKquerytemplate = f"https://www.google.com/search?q={search_query}&rlz=1C1CHBF_en-GBGB921GB921&oq=ping&aqs=chrome..69i57j46i433j46i199i291i433j0i433l4j0.1173j0j7&sourceid=chrome&ie=UTF-8"
    chfmi = "Click here for more information"
    foot = "Please note that this may only work for residents in the UK."
    e = discord.Embed(title=f"{ctx.author.name} searched for... {search_query}.",
                      description="**[{}]({})**".format(chfmi, UKquerytemplate),
                      colour=discord.Colour.red())
    e.set_footer(text=footer)
    await ctx.send(e=embed)
