import discord
import asyncio
from redbot.core import commands
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicates

class FestiveCards(commands.Cog):
  """Send someone a christmas card!"""
  
  def __init__(self, bot):
    self.bot = bot

  @commands.group()
  async def card(self, ctx):
    """Send a christmas card to someone!"""
      
  @card.group()
  async def send(self, ctx):
    """Send a card to someone!"""
  
  @card.command()
  async def viewoutput(self, ctx):
    """Send a template version to your DM!"""
    can_react = ctx.channel.permissions_for(ctx.me).add_reactions
    if can_react:
      message = await ctx.send(
        "Which card type would you like to see? Please react accordingly.\n"
        "These reactions will be removed after **20 seconds**.\n"
        "\n`❄️`: **Christmas**"
        "\n`🎂`: **Birthday**"
        "\n`🏥`: **Get Well Soon**"
      )
      reactions = ReactionPredicate.with_emojis(("❄️", "🎂", "🏥"), message, user)
      start_adding_reactions(message, reactions)
      pred = ReactionPredicate.with_emojis(emojis, msg)
      await asyncio.sleep(20)
      await reactions.clear()
      await reactions.clear.send(f"Timed out. Please try again using {ctx.clean_prefix}.")
    else:
      await ctx.send("I don't have permissions to add reactions.")
    

  @card.command()
  async def christmas(self, ctx: commands.Context, user_id: int, *, message: str):
    """Send a christmas card to someone!"""
    destination = self.bot.get_user(user_id)
    author = ctx.author.name
    user = destination
    if destination is None or destination.bot:
        await ctx.send("Invalid ID, user not found, or user is a bot.")
    foot = (f"Send christmas cards using {ctx.clean_prefix}card!")
    e = discord.Embed(title=f":christmas_tree: Christmas Card from {ctx.author} :christmas_tree:", 
                      description= "Dear {},\n\n{}\n\nFrom {} :gift:".format(user.name, message, author), 
                      colour=discord.Colour.red())
    e.set_footer(text=foot)
    try:
      await destination.send(embed=e)
    except discord.HTTPException:
      await ctx.send(f"Sorry, I couldn't send a card to **{user.name}.**")
    else:
      await ctx.send(f"Christmas card delivered to **{user.name}!** :gift:")
