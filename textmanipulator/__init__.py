  
from .textmanipulator import TextManipulator

def setup(bot):
  bot.add_cog(TextManipulator(bot))