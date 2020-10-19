from .zuko import Zuko

async def setup(bot):
    cog = Zuko()
    bot.add_cog(cog)
