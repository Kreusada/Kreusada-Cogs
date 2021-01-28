from .codify import Codify

def setup(bot):
    bot.add_cog(Codify(bot))