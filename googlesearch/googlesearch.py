from redbot.core import commands
import discord

class GoogleSearch(commands.Cog):
  
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  async def google(self, ctx, search_query: str):
    """Search google with a simple URL."""
    joinwords = "%".join(search_query)
    querytemplate = f"https://www.google.com/search?q={joinwords}"
    chfmi = "Click here for more information"
    footer = f"Search google by using: {ctx.clean_prefix}google <search_query>"
    e = discord.Embed(title=f"{ctx.author.name} searched for... {search_query}.",
                      description="**[{}]({})**".format(chfmi, querytemplate),
                      colour=discord.Colour.red())
    e.set_footer(text=footer)
    await ctx.send(embed=e)
