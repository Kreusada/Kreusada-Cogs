import unicodedata
from typing import Any, Optional

import discord
from discord.interactions import Interaction
from redbot.core.commands import Context


def alpha_2_to_unicode(alpha_2):
    return "".join(unicodedata.lookup("REGIONAL INDICATOR SYMBOL LETTER " + a) for a in alpha_2)


class LabelledMenuSelect(discord.ui.Select):
    def __init__(self, neighbours: dict[str, str]):
        options = [discord.SelectOption(label=k, emoji=v) for k, v in neighbours.items()]
        super().__init__(placeholder="Neighbouring countries", options=options, row=1)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Get information about {self.values[0]} with the command `{self.view.context.clean_prefix}flag {self.values[0]}`!",
            ephemeral=True,
        )


class LabelledMenuButton(discord.ui.Button):
    async def callback(self, interaction: discord.Interaction):
        self.grey_all_buttons()
        self.style = discord.ButtonStyle.green
        await interaction.response.edit_message(
            view=self.view, **self.view.options[self.label]["kwargs"]
        )

    def grey_all_buttons(self):
        for button in self.view.children:
            button.style = discord.ButtonStyle.grey


class LabelledMenu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.context: Optional[Context] = None
        self.options: dict[str, discord.Embed] = {}
        self.select: Optional[discord.ui.Select] = None
        self.__insertion_order: list[str] = []

    def add_option(
        self,
        label: str,
        /,
        content: Optional[str] = None,
        *,
        embed: Optional[discord.Embed] = None,
        emoji: Optional[str] = None,
    ):
        self.options[label] = {"emoji": emoji, "kwargs": {"embed": embed, "content": content}}
        self.__insertion_order.append(label)
        self.add_item(LabelledMenuButton(label=label, emoji=emoji, row=2))

    def set_neighbouring_countries(self, neighbours: dict[str, str]):
        if not neighbours:
            return
        self.add_item(LabelledMenuSelect(neighbours))

    async def start(self, ctx: Context):
        self.context = ctx
        self.children[0].style = discord.ButtonStyle.green
        self.message = await ctx.send(
            **self.options[self.__insertion_order[0]]["kwargs"], view=self
        )

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.context.author.id:
            await interaction.response.send_message(
                "You are not allowed to interact with this.", ephemeral=True
            )
            return False
        return True
