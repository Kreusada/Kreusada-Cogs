from .getrole import Getrole

async def setup(bot):
    cog = Getrole()
    bot.add_cog(cog)
