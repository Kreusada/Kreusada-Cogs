from .timestamps import TimeStamps, __red_end_user_data_statement__


async def setup(bot):
    await bot.add_cog(TimeStamps(bot))
