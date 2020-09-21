from .coll import Collectable


def setup(bot):
    bot.add_cog(Collectable(bot))
