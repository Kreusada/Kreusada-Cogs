from .scanner import YamlScanner

def setup(bot):
    bot.add_cog(YamlScanner(bot))