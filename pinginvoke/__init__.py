from .pingi import PingInvoke, __red_end_user_data_statement__


async def setup(bot):
    cog = PingInvoke(bot)
    await bot.add_cog(cog)
