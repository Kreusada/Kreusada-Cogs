from .scanner import JsonScanner

def setup(bot):
    bot.add_cog(JsonScanner(bot))