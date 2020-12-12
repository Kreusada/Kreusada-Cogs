from .sendcards import SendCards

def setup(bot):
  bot.add_cog(SendCards(bot))
