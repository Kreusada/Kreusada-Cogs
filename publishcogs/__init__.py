from .publishcogs import PublishCogs

def setup(bot):
    bot.add_cog(PublishCogs(bot))