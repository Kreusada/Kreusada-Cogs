from .voicenick import VoiceNick

__red_end_user_data_statement__ = "This cog does not persistently store data about users."

def setup(bot):
    cog = VoiceNick(bot)
    bot.add_cog(cog)