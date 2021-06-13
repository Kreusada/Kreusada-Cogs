import contextlib
import discord

from redbot.core import commands
from redbot.core.utils.chat_formatting import box, pagify

kreuslang = {
    "a": "^<.", "b": "^-.", "c": "^>.", "d": "~<.",
    "e": "~-.", "f": "~>.", "g": "_<.", "h": "_-.",
    "i": "_>.", "j": "^<..", "k": "^-..", "l": "^>..",
    "m": "~<..", "n": "~-..", "o": "~>..", "p": "_<..",
    "q": "_-..", "r": "_>..", "s": "^<...", "t": "^-...",
    "u": "^>...", "v": "~<...", "w": "~-...", "x": "~>...",
    "y": "_<...", "z": "_-...", " ": "/"
}

def toenglish(text):
    data = {v: k for k, v in kreuslang.items()}
    ret = []
    for i in text.split(","):
        if i == "/":
            ret.append(" ")
            continue
        ret.append(data[i])
    return "".join(ret)

def tokreulang(text):
    ret = []
    text = text.lower()
    for let in list(text):
        if let.isspace():
            ret.append("/")
            continue
        if not let.isalnum():
            continue
        let = let.lower()
        ret.append(kreuslang[let])
    return ",".join(ret)

class KreuLang(commands.Cog):
    """My language :smile:"""

    @commands.group()
    async def kreulang(self, ctx):
        """Translate kreulang"""

    @kreulang.command()
    async def decode(self, ctx, *, kreulang: str):
        """Translate kreulang to english"""
        for page in pagify(toenglish(kreulang), page_length=1993):
            await ctx.send(box(page, lang="yaml"))

    @kreulang.command()
    async def encode(self, ctx, *, english: str):
        """Translate english to kreulang"""
        for page in pagify(tokreulang(english), page_length=1993):
            await ctx.send(box(page, lang="yaml"))

    @commands.Cog.listener()
    async def on_message_without_command(self, message):
        if not message.channel.id in (853716880010117120, 853717911768399882):
            return
        if message.author.bot:
            return
        for m in message.content.split():
            if m.isalnum():
                with contextlib.suppress(discord.HTTPException):
                    await message.delete()
                await message.channel.send(f"{message.author.mention} Please only use kreulang in this channel.", delete_after=3)