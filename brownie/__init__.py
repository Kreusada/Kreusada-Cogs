from .brownie import Brownie

async def setup(bot):
    """Load Brownie cog."""
    cog = Brownie(bot)
    bot.add_cog(cog)
