from .getrole import Getrole


def setup(bot):
    bot.add_cog(Getrole(bot))
