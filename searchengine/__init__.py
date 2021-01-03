from .searchengine import SearchEngine

__red_end_user_data_statement__ = "This cog does not persistently store data about users."

def setup(bot):
  bot.add_cog(SearchEngine(bot))
