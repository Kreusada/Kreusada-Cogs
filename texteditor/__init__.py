from .texteditor import TextEditor, __red_end_user_data_statement__


def setup(bot):
    cog = TextEditor(bot)
    bot.add_cog(cog)
