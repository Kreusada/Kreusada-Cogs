import random

import discord
from redbot.core import commands

RIDDLES = [
    {"riddle": "What has keys but can't open locks?", "answer": "A piano"},
    {"riddle": "What runs but never walks, has a mouth but never talks?", "answer": "A river"},
    {"riddle": "What can travel around the world while staying in a corner?", "answer": "A stamp"},
    {"riddle": "What has a head, a tail, is brown, and has no legs?", "answer": "A penny"},
    {
        "riddle": "What comes once in a minute, twice in a moment, but never in a thousand years?",
        "answer": "The letter M",
    },
    {"riddle": "What is full of holes but still holds water?", "answer": "A sponge"},
    {"riddle": "What is always in front of you but can’t be seen?", "answer": "The future"},
    {"riddle": "What has a heart that doesn’t beat?", "answer": "An artichoke"},
    {"riddle": "What has to be broken before you can use it?", "answer": "An egg"},
    {
        "riddle": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
        "answer": "An echo",
    },
    {"riddle": "The more you take, the more you leave behind. What am I?", "answer": "Footsteps"},
    {
        "riddle": "I’m tall when I’m young, and I’m short when I’m old. What am I?",
        "answer": "A candle",
    },
    {
        "riddle": "What has cities, but no houses; forests, but no trees; and rivers, but no water?",
        "answer": "A map",
    },
    {
        "riddle": "What is seen in the middle of March and April that can’t be seen at the beginning or end of either month?",
        "answer": "The letter R",
    },
    {
        "riddle": "You see me once in June, twice in November, but not at all in May. What am I?",
        "answer": "The letter E",
    },
    {"riddle": "I have branches, but no fruit, trunk or leaves. What am I?", "answer": "A bank"},
    {"riddle": "What can you catch, but not throw?", "answer": "A cold"},
    {
        "riddle": "If you drop me, I’m sure to crack, but give me a smile and I’ll always smile back. What am I?",
        "answer": "A mirror",
    },
    {"riddle": "What has legs but doesn’t walk?", "answer": "A table"},
    {"riddle": "What has one eye, but can’t see?", "answer": "A needle"},
    {"riddle": "What gets wetter as it dries?", "answer": "A towel"},
    {
        "riddle": "What has a bed but never sleeps, can run but never walks, and has a bank but no money?",
        "answer": "A river",
    },
    {"riddle": "What word is spelled incorrectly in every dictionary?", "answer": "Incorrectly"},
    {"riddle": "What begins with T, ends with T, and has T in it?", "answer": "A teapot"},
    {"riddle": "Forward I am heavy, but backward I am not. What am I?", "answer": "A ton"},
    {"riddle": "What has hands, but can’t clap?", "answer": "A clock"},
    {"riddle": "What goes up but never comes down?", "answer": "Your age"},
    {"riddle": "What has four wheels and flies?", "answer": "A garbage truck"},
    {"riddle": "What comes down but never goes up?", "answer": "Rain"},
    {"riddle": "What is so fragile that saying its name breaks it?", "answer": "Silence"},
    {"riddle": "What can fill a room but takes up no space?", "answer": "Light"},
    {"riddle": "What begins with an E but only has one letter?", "answer": "An envelope"},
    {"riddle": "What has a neck but no head?", "answer": "A bottle"},
    {"riddle": "What belongs to you but is used more by others?", "answer": "Your name"},
    {
        "riddle": "I’m light as a feather, yet the strongest man can’t hold me for more than 5 minutes. What am I?",
        "answer": "Your breath",
    },
    {
        "riddle": "What is black when it’s clean and white when it’s dirty?",
        "answer": "A chalkboard",
    },
    {
        "riddle": "I’m not alive, but I can grow; I don’t have lungs, but I need air; I don’t have a mouth, and I can drown. What am I?",
        "answer": "A fire",
    },
    {"riddle": "The more of this there is, the less you see. What is it?", "answer": "Darkness"},
    {"riddle": "What has a ring but no finger?", "answer": "A telephone"},
    {"riddle": "What has one head, one foot, and four legs?", "answer": "A bed"},
    {"riddle": "What can’t be put in a saucepan?", "answer": "Its lid"},
    {"riddle": "What has 13 hearts, but no other organs?", "answer": "A deck of cards"},
    {"riddle": "What has words, but never speaks?", "answer": "A book"},
    {"riddle": "What has a bottom at the top?", "answer": "Your legs"},
    {"riddle": "What kind of room has no doors or windows?", "answer": "A mushroom"},
    {"riddle": "What kind of tree can you carry in your hand?", "answer": "A palm"},
    {"riddle": "What gets bigger the more you take away?", "answer": "A hole"},
    {"riddle": "I shave every day, but my beard stays the same. What am I?", "answer": "A barber"},
    {"riddle": "What tastes better than it smells?", "answer": "Your tongue"},
    {"riddle": "What has a thumb and four fingers but is not alive?", "answer": "A glove"},
    {"riddle": "What has no beginning, end, or middle?", "answer": "A doughnut"},
    {
        "riddle": "What is always hungry, must be fed, but dies when given a drink?",
        "answer": "Fire",
    },
    {
        "riddle": "What can you hold in your left hand but not in your right?",
        "answer": "Your right elbow",
    },
    {"riddle": "What can be cracked, made, told, and played?", "answer": "A joke"},
    {
        "riddle": "What starts with a P, ends with an E, and has thousands of letters?",
        "answer": "The post office",
    },
    {
        "riddle": "What word of five letters has only one left when two letters are removed?",
        "answer": "Stone",
    },
    {"riddle": "What is harder to catch the faster you run?", "answer": "Your breath"},
    {
        "riddle": "I am an odd number. Take away one letter and I become even. What number am I?",
        "answer": "Seven",
    },
    {"riddle": "What has a bark but no bite?", "answer": "A tree"},
    {"riddle": "What invention lets you look right through a wall?", "answer": "A window"},
    {
        "riddle": "What has a lock but no key, can be put in a hole but not dug out?",
        "answer": "A padlock",
    },
    {
        "riddle": "What five-letter word becomes shorter when you add two letters to it?",
        "answer": "Short",
    },
    {"riddle": "What can you keep after giving it to someone?", "answer": "Your word"},
    {
        "riddle": "What word is pronounced the same if you take away four of its five letters?",
        "answer": "Queue",
    },
    {"riddle": "What has many teeth but can’t bite?", "answer": "A comb"},
    {"riddle": "What has an eye but cannot see?", "answer": "A needle"},
    {"riddle": "What is always coming but never arrives?", "answer": "Tomorrow"},
    {"riddle": "What gets sharper the more you use it?", "answer": "Your brain"},
    {
        "riddle": "What has roots as nobody sees, is taller than trees. Up, up it goes, and yet never grows?",
        "answer": "A mountain",
    },
    {
        "riddle": "What is as light as a feather, yet the world’s strongest man couldn’t hold it for much longer than a minute?",
        "answer": "His breath",
    },
    {
        "riddle": "What comes once in a year, twice in a month, four times in a week, and six times in a day?",
        "answer": "The letter E",
    },
    {"riddle": "What goes through cities and fields, but never moves?", "answer": "A road"},
    {"riddle": "What can fill a room but is invisible?", "answer": "Air"},
    {"riddle": "What is so light that a feather can’t hold it down?", "answer": "A soap bubble"},
    {"riddle": "What comes down but never goes up?", "answer": "Rain"},
    {"riddle": "What has a head, a tail, is brown, and has no legs?", "answer": "A penny"},
    {"riddle": "What is always in front of you but can’t be seen?", "answer": "The future"},
    {
        "riddle": "What word is spelled the same forwards, backwards, and upside down?",
        "answer": "NOON",
    },
    {
        "riddle": "What is greater than God, more evil than the devil, the poor have it, the rich need it, and if you eat it, you die?",
        "answer": "Nothing",
    },
    {
        "riddle": "What can you hold without ever touching or using your hands?",
        "answer": "Your breath",
    },
    {
        "riddle": "What begins with the letter 'I', and by adding a letter, you become silent?",
        "answer": "Island",
    },
    {"riddle": "What has a bed but never sleeps?", "answer": "A river"},
    {
        "riddle": "I am taken from a mine, and shut up in a wooden case, from which I am never released, and yet I am used by almost every person. What am I?",
        "answer": "A pencil",
    },
    {"riddle": "What has a face and two hands, but no arms or legs?", "answer": "A clock"},
]


class ViewAnswer(discord.ui.View):
    def __init__(self, answer: str) -> None:
        super().__init__(timeout=300)
        self.answer = answer

    @discord.ui.button(emoji="\N{BRAIN}", label="View Answer", style=discord.ButtonStyle.secondary)
    async def _view_answer(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.response.is_done():
            await interaction.followup.send(f"{self.answer}", ephemeral=True)
        else:
            await interaction.response.send_message(f"{self.answer}", ephemeral=True)


class Riddles(commands.Cog):
    """Get a random riddle."""

    __version__ = "1.0.1"
    __author__ = "Kreusada"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete."""
        return

    @commands.command()
    async def riddle(self, ctx: commands.Context):
        """Get a random riddle."""
        choice = random.choice(RIDDLES)
        await ctx.send(
            f"\N{BLACK QUESTION MARK ORNAMENT}\N{VARIATION SELECTOR-16} {choice['riddle']}",
            view=ViewAnswer(choice["answer"]),
        )
