from .zuko import Zuko


def setup(bot):
    bot.add_cog(Zuko(bot))
