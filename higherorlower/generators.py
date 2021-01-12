import discord
from random import choice, randint
from .cards import (
    C2, C3, C4, C5, C6,
    C7, C8, C9, C10, JACK,
    QUEEN, KING, ACE, HONORS
)

async def embed(a: discord.Member, n: int, config: bool, count: int, qs: int):
    if n == 2:
        image = choice(C2)
        num = n
    elif n == 3:
        image = choice(C3)
        num = n
    elif n == 4:
        image = choice(C4)
        num = n
    elif n == 5:
        image = choice(C5)
        num = n
    elif n == 6:
        image = choice(C6)
        num = n
    elif n == 7:
        image = choice(C7)
        num = n
    elif n == 8:
        image = choice(C8)
        num = n
    elif n == 9:
        image = choice(C9)
        num = n
    elif n == 10:
        image = choice(C10)
        num = n
    elif n == 11:
        image = choice(JACK)
        num = "Jack (11)"
    elif n == 12:
        image = choice(QUEEN)
        num = "Queen (12)"
    elif n == 13:
        image = choice(KING)
        num = "King (13)"
    else:
        image = choice(ACE)
        num = "Ace (14)"
    embed = discord.Embed(title=f"{a}, your card is a {num}.", description="Higher or Lower?", color=0xFF0000)
    embed.set_footer(text=f"Cards: {count}/{qs}")
    if config is True:
        embed.set_image(url=image)
    else:
        embed.set_thumbnail(url=image)
    return embed
    
