from .githubskylines import GithubSkylines

def setup(bot):
    bot.add_cog(GithubSkylines(bot))