from .collectables import Collectables


def setup(bot):
    bot.add_cog(Collectables(bot))
