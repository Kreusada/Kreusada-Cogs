import discord
from redbot.core import commands

class ChristmasCard(commands.Cog):
  """Send someone a christmas card!"""
  
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def card(self, ctx: commands.Context, user_id: int, *, message: str):
    """Send a christmas card to someone!"""
    destination = self.bot.get_user(user_id)
    if destination is None or destination.bot:
        await ctx.send("Invalid ID, user not found, or user is a bot.")
    foot = (f"Send christmas cards using {ctx.clean_prefix}card!")
    e = discord.Embed(title=f":christmas_tree: Christmas Card from {ctx.author} :christmas_tree:", 
                      description= f"Dear {user.name}, message, colour=discord.Colour.red())
    e.set_footer(text=foot)
    try:
      await destination.send(embed=e)
    except discord.HTTPException:
      await ctx.send("Sorry, I couldn't send a card to {}").format(destination)
    else:
      await ctx.send(f"Message delivered to {destination}")
    response = (f"{description}\nMessage:\n\n{message}")
    try:
        await destination.send(f"{box(response)}\n{content}")
    except discord.HTTPException:
        await ctx.send(f"Sorry, I couldn't deliver your message to {destination}")
    else:
        await ctx.send(f"Message delivered to {destination}")
