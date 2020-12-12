import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box

class FestiveCards(commands.Cog):
  """Send someone a christmas card!"""
  
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def card(self, ctx: commands.Context, user_id: int, *, message: str):
    """Send a christmas card to someone!"""
    destination = self.bot.get_user(user_id)
    username = user.name
    author = ctx.author.name
    user = destination
    if destination is None or destination.bot:
        await ctx.send("Invalid ID, user not found, or user is a bot.")
    foot = (f"Send christmas cards using {ctx.clean_prefix}card!")
    e = discord.Embed(title=f":christmas_tree: Christmas Card from {ctx.author} :christmas_tree:", 
                      description= "Dear {},\n\n{}\n\nFrom {} :gift:".format(username, message, author), 
                      colour=discord.Colour.red())
    e.set_footer(text=foot)
    try:
      await destination.send(embed=e)
    except discord.HTTPException:
      await ctx.send("Sorry, I couldn't send a card to {}").format(username)
    else:
      await ctx.send(f"Message delivered to {username}")
