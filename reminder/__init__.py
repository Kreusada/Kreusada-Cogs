from .reminder import Reminder

def setup(bot):
  bot.add_cog(Reminder(bot))
