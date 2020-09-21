from .coll import Coll


def setup(bot):
    bot.add_cog(Coll(bot))
