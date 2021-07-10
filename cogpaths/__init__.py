from .cogpaths import CogPaths, __red_end_user_data_statement__


async def setup(bot):
    cog = CogPaths(bot)
    await cog.initialize()
    bot.add_cog(cog)
