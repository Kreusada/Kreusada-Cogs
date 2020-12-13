from .searchpinterest import SearchPinterest

def setup(bot):
  bot.add_cog(SearchPinterest(bot))
