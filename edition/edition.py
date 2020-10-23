import discord
from redbot.core import commands, checks, Config

class Edition(commands.Cog):
   """Edition"""

   @commands.command()
   async def edition(self, ctx, *, name: str = None): 
      """Become an edition of Kreusada."""
   if name is None: 
      await ctx.author.edit(nick=ctx.author.name) 
      return await ctx.send("Your nickname was reset.")
   user = ctx.author
   before = ctx.author.name
   after = name
   tag = "Kreusada - {0} Edition".format(after)
   try:
      await user.edit(nick=tag)
      except discord.Forbidden:
         await ctx.send("Your nickname could not be changed, I don't have permissions or you are higher than me in the role heirarchy.")
      
      await ctx.send("You are now an Edition of Kreusada. Your nickname was successfully changed to: ``{}``".format(tag))
