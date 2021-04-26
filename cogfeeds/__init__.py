from .cogfeeds import CogFeeds

def setup(bot):
    bot.add_cog(CogFeeds(bot))