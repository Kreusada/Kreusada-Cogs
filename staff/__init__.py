from .staff import Staff

def setup(bot):
    cog = Staff(bot)
    bot.add_cog(cog)
