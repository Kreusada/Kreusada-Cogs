from .version import Vinfo

def setup(bot):
    bot.add_cog(Vinfo(bot))