from .guildblocklist import GuildBlocklist

def setup(bot):
    bot.add_cog(GuildBlocklist(bot))