from .publishcogs import PublishCogs

def setup(bot):
  bot.add_cog(PublishCogs(bot))

__red_end_user_data_statement__ = "This cog does not persistently store data about users."
