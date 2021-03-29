from .serverblock import ServerBlock


def setup(bot):
    bot.add_cog(ServerBlock(bot))