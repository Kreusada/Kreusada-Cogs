from .texteditor import __red_end_user_data_statement__, TextEditor

def setup(bot):
    cog = TextEditor(bot)
    bot.add_cog(cog)
