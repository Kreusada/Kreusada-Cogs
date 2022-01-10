from .roleboards import RoleBoards


def setup(bot):
    cog = RoleBoards(bot)
    bot.add_cog(cog)
