import discord
from redbot.core import commands, checks
from redbot.cogs.downloader.converters import InstalledCog

class Cogtools(commands.Cog):
  
  @commands.is_owner()
  @commands.command()
  async def updr(ctx, *cogs: InstalledCog):
    """Update cogs without questioning about reload."""
    ctx.assume_yes = True
    cog_update_command = ctx.bot.get_command("cog update")
    if cog_update_command is None:
        await ctx.send(
          f"I can't find {ctx.prefix}cog update command"
        )
        return
    await ctx.invoke(cog_update_command, *cogs)
    return updr
