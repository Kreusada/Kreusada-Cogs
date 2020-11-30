import discord
from redbot.core import commands, checks
from redbot.cogs.downloader.converters import InstalledCog

class Cogtools(commands.Cog):
  """Tools for cogs."""
  
  def __init__(self, bot):
    self.bot = bot
  
    @commands.command()
    @commands.max_concurrency(1)
    @commands.is_owner()
    async def updreload(self, ctx: commands.Context):
        """Updates installed cogs and reloads the loaded ones automatically."""
        ctx.assume_yes = True
        cog_upd_command = ctx.bot.get_command("cog update")
        if cog_upd_command is None:
            await ctx.send("Welp, that ain't gonna happen. \nYou need to `{}load downloader` first.".format(ctx.prefix))
        else:
            await ctx.invoke(cog_upd_command)
