from .searchengine import SearchEngine

def setup(bot):
  bot.add_cog(SearchEngine(bot))
