from .outofcontext import OutOfContext

def setup(bot):
  bot.add_cog(OutOfContext(bot))
