import discord
from redbot.core import commands

class AntiBotRole(commands.Cog):
  """Invite a bot to your server without their automated role."""
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command(aliases=["botinv"])
  async def invbot(self, ctx, bot_id: int):
    user = self.bot.get_user(bot_id)
    if user.bot is True:
      bot = self.bot
      inv = f"https://discord.com/oauth2/authorize?client_id={bot_id}&scope=bot"
      chti = "Click here to invite"
      e = discord.Embed(title=f"{user.name} Invite Link (Without Role)",
                        description="**ID: {}**\n\n**[{}]({})**".format(user.id, chti, inv),
                        color=0xb7fff3)
      e.set_author(name=bot.user.name, icon=bot.user.avatar_url)                  
      await ctx.send(embed=e)
    else:
      await ctx.send(f"Please enter a valid bot ID. **{bot_id} was not recognised.**")
    
def setup(bot):
  bot.add_cog(AntiBotRole(bot))
