from .pingi import PingInvoke


def setup(bot):
    bot.add_cog(PingInvoke(bot))