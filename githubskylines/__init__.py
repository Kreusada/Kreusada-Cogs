from .githubskylines import GithubSkylines


async def setup(bot):
    cog = GithubSkylines(bot)
    await cog.initialize()
    bot.add_cog(cog)
