from .shoppingcart import ShoppingCart

def setup(bot):
  bot.add_cog(ShoppingCart(bot))