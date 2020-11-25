import discord
from redbot.core import commands, checks, Config

class Edition(commands.Cog):
   """Become an edition of someone!\n"""
   """Inspired from the Red main server."""
   
   @commands.command()
   async def editionset(self, ctx, user: str):
      """Who is your 'edition' guy?"""
      await self.config.guild(ctx.guild).set_raw(edition)
      await ctx.send("Edition 'guy' set.")
      
   @commands.command()
   async def edition(self, ctx, *, name: str = None): 
      """Become an edition."""
      if name is None: 
         await ctx.author.edit(nick=ctx.author.name) 
         return await ctx.send("Your nickname was reset.")
      user = ctx.author
      before = ctx.author.name
      after = name
      editioner = await self.config.guild(ctx.guild).get_raw(edition)
      tag = "{} - {0} Edition".format(editioner, after)
      try: 
         await user.edit(nick=tag)
      except discord.Forbidden: 
         await ctx.send("Your nickname could not be changed, I don't have permissions or you are higher than me in the role heirarchy.")
      
      await ctx.send(f"You are now an Edition of Kreusada. Your nickname was successfully changed to: ``{tag}``.")
