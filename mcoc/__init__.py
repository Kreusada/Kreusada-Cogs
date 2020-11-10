from .mcoc import Mcoc

async def setup(bot):
    cog = Mcoc(bot)
    bot.add_cog(cog)
