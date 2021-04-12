from .spoilerchannel import SpoilerChannel

def setup(bot):
    bot.add_cog(SpoilerChannel(bot))