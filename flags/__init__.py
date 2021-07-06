from .flags import Flags


def setup(bot):
    bot.add_cog(Flags(bot))
