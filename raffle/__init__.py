from .raffle import Raffle

async def setup(bot):
    cog = Raffle(bot)
    await cog.initialize()
    bot.add_cog(cog)