from .voicenick import VoiceNick

def setup(bot):
    cog = VoiceNick(bot)
    bot.add_cog(cog)