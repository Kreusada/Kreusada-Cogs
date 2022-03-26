from .raffle import Raffle, __red_end_user_data_statement__


async def setup(bot):
    cog = Raffle(bot)
    await cog.initialize()
    await bot.add_cog(cog)
