from redbot.core import commands

class champ(commands.Cog):
    """Retrieves champion portrait and featured images."""

@commands.group()
async def testembed(self, ctx):
  pass

@testembed.command
async def one(self, ctx):
    embedVar1 = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    embedVar1.add_field(name="Field1", value="hi", inline=False)
    embedVar1.add_field(name="Field2", value="hi2", inline=False)
    await ctx.send(embed=embedVar)
