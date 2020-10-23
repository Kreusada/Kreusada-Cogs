from .get import Get


def setup(bot):
    bot.add_cog(Get(bot))
