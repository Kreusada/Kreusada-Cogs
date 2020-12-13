from .searchgoogle import SearchGoogle

def setup(bot):
  bot.add_cog(SearchGoogle(bot))
