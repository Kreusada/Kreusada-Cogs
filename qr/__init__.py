from .qr import QR


def setup(bot):
    bot.add_cog(QR(bot))
