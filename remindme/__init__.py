from .remindme import RemindMe

def setup(bot):
  bot.add_cog(RemindMe(bot))