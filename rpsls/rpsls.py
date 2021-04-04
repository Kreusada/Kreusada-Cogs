# Made for TW on Discord
import json
from pathlib import Path
from random import choice as pick, randint

import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import bold

rock = "\N{MOYAI}"
paper = "\N{PAGE FACING UP}"
scissors = "\N{BLACK SCISSORS}\N{VARIATION SELECTOR-16}"
lizard = "\N{LIZARD}"
spock = "\N{RAISED HAND WITH PART BETWEEN MIDDLE AND RING FINGERS}"

choices = ["scissors", "paper", "rock", "lizard", "spock"]

emojis = {
    0: scissors,
    1: paper,
    2: rock,
    3: lizard,
    4: spock,
}

class RPSLS(commands.Cog):
    """Rock, paper, scizzors, lizard, spock."""

    __author__ = "Kreusada"
    __version__ = "1.0.0"

    def __init__(self, bot):
        self.bot = bot
        self.converter = lambda x: choices.index(x.lower())

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command()
    async def rpsls(self, ctx, choice: str):
        """
        Play rock, paper, scizzors, lizard, spock.
        
        Use `[p]rpsls help` for a diagram."""
        choice = choice.lower()
        if choice == "help":
            with open(Path(__file__).parent / "info.json") as fp:
                return await ctx.send(json.load(fp)["diagram"])
        if not choice in choices:
            return await ctx.send("Please enter a valid choice.")
        b = self.converter(pick(choices))
        h = self.converter(choice)
        k = {0:[1,3],1:[2,4],2:[3,0],3:[4,1],4:[0,2]}
        if h == b:
            title = f"{emojis[h]} vs {emojis[b]}"
            description = f"It's a draw."
            color = 0x87ceeb
        elif b in k[h]:
            title = f"{emojis[h]} vs {emojis[b]}"
            description = f"You win!"
            color = 0x22ce70
        else:
            title = f"{emojis[h]} vs {emojis[b]}"
            description = f"{ctx.me.name} wins."
            color = 0xff5151
        kwargs = {"title": title,"description": description, "color": color}
        if await ctx.embed_requested():
            await ctx.send(embed=discord.Embed(**kwargs))
        else:
            await ctx.send(bold(title) + '\n' + description)

