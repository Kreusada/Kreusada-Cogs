from .githubskyline import GithubSkyline

def setup(bot):
    bot.add_cog(GithubSkyline(bot))