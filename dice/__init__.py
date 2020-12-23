from .dice import Dice

def setup(bot):
  bot.add_cog(Dice(bot))
