from .dehoister import Dehoister, __red_end_user_data_statement__


async def setup(bot):
    cog = Dehoister(bot)
    await bot.add_cog(cog)
