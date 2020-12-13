from .abs import AppendBackslash

def setup(bot):
  bot.add_cog(AppendBackslash(bot))
