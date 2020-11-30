import discord
from redbot.core import commands, checks
from redbot.cogs.downloader.converters import InstalledCog

class L(commands.Cog):
  """private learning"""
  
  def __init__(self, bot):
    self.bot = bot
  
    @bot.event
    async def on_message(message):
      if message.author == bot.user:
        return
      
      if message.content.startswith("Demaratus"):
      async def updreload(self, ctx: commands.Context):
          ctx.assume_yes = True
          cog_upd_command = ctx.bot.get_command("cog update")
          if cog_upd_command is None:
              await ctx.send("Welp, that ain't gonna happen. \nYou need to `{}load downloader` first.".format(ctx.prefix))
          else:
              await ctx.invoke(cog_upd_command)
