import discord

from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands import Context
from redbot.core.utils.chat_formatting import quote

from operator import itemgetter
from typing import Optional


CARD_TYPES_DATA = [
    {
        "name": "Christmas",
        "description": "Send a Christmas card",
        "emoji": "\U0001f384",
        "prompt": "Merry Christmas, {recipient}!",
        "colour": 0x2B730A,
    },
    {
        "name": "Halloween",
        "description": "Send a Halloween card",
        "emoji": "\U0001f383",
        "prompt": "Happy halloweeeeen \U0001f47b",
        "colour": 0xEB5A0C,
    },
    {
        "name": "Get well soon",
        "description": "Wish someone a speedy recovery",
        "emoji": "\U0001f321",
        "prompt": "Hope you feel better soon \U0001f622",
        "colour": 0xFFD4D4,
    },
    {
        "name": "Birthday",
        "description": "Send a Birthday card",
        "emoji": "\U0001f389",
        "prompt": "Happy birthday! \U0001f382",
        "colour": 0x63B4C2,
    },
    {
        "name": "Valentines",
        "description": "Send a Valentines day card",
        "emoji": "\U0001f497",
        "prompt": "Happy valentines day <3",
        "colour": 0xD92E2E,
    },
    {
        "name": "Wedding",
        "description": "Wish someone well on their wedding day",
        "emoji": "\U0001f492",
        "prompt": "Best wishes for a fun-filled future together.",
        "colour": 0xFFFFFF,
    },
    {
        "name": "New house",
        "description": "Congratulate someone on getting a new house",
        "emoji": "\U0001f3e1",
        "prompt": "Congrats on your new house!",
        "colour": 0xCFCF48,
    },
    {
        "name": "New years",
        "description": "Wish someone a happy new year",
        "emoji": "\U0001f942",
        "prompt": "Happy new year!!! \U0001f942\U0001f942",
        "colour": 0xFCF52B,
    },
    {
        "name": "Confession",
        "description": "Make a confession to someone",
        "emoji": "\U0001f48c",
        "prompt": "Hey, uhhh... [insert cheesy phrase here]",
        "colour": 0x814EBA,
    },
    {
        "name": "Thank you",
        "description": "Thank someone in a card",
        "emoji": "\U0001f64f",
        "prompt": "Thanks for everything!",
        "colour": 0x3BCC86,
    },
    {
        "name": "Anniversary",
        "description": "Wish someone well on their anniversary",
        "emoji": "\U0001f48d",
        "prompt": "Happy anniversary to you and your partner!",
        "colour": 0x60D6A9,
    },
    {
        "name": "Condolences",
        "description": "Provide someone some emotional support",
        "emoji": "\U0001f54a",
        "prompt": "May the love of those around you help you through the days ahead...",
        "colour": 0xFFFFFF,
    },
    {
        "name": "Fortune",
        "description": "Send a good luck card",
        "emoji": "\U0001f340",
        "prompt": "Best of luck with your new project!",
        "colour": 0x7CA53E,
    },
    {
        "name": "New baby",
        "description": "Congratulate someone on their new baby",
        "emoji": "\U0001f476",
        "prompt": "Congrats on your new baby \U0001f979",
        "colour": 0x89CFF0,
    },
    {
        "name": "Graduation",
        "description": "Congratulate someone on their graduation",
        "emoji": "\U0001f393",
        "prompt": "Congrats on the graduation!",
        "colour": 0x000000,
    },
    {
        "name": "Retirement",
        "description": "Wish someone well for their retirement",
        "emoji": "\U0001f9d3",
        "prompt": "You can relax a tad more now...",
        "colour": 0x808080,
    },
    {
        "name": "Congratulations",
        "description": "Congratulate someone on a recent success",
        "emoji": "\U0001f38a",
        "prompt": "Congratulations! You did so well.",
        "colour": 0x446DD4,
    },
]

CARD_TYPES_DATA = sorted(CARD_TYPES_DATA, key=itemgetter("name"))


class CardSelect(discord.ui.Select):
    def __init__(
        self,
        ctx: Context,
        /,
        *,
        sender: discord.User,
        recipient: discord.User,
        card_content: Optional[str] = None,
    ):
        options = [
            discord.SelectOption(
                label=card["name"],
                description=card["description"],
                emoji=card["emoji"],
                value=index,
            )
            for index, card in enumerate(CARD_TYPES_DATA)
        ]
        self.ctx = ctx
        self.recipient = recipient
        self.sender = sender
        self.card_content = card_content
        super().__init__(placeholder="Select a card", options=options)

    async def callback(self, interaction: discord.Interaction):
        modal = CardBodyModal(
            self.ctx,
            sender=self.sender,
            recipient=self.recipient,
            card_index=int(self.values[0]),
            card_content=self.card_content,
        )
        await interaction.response.send_modal(modal)


class CardSelectView(discord.ui.View):
    def __init__(
        self,
        ctx: Context,
        *,
        sender: discord.User,
        recipient: discord.User,
        card_content: Optional[str] = None,
    ):
        super().__init__(timeout=100)
        self.ctx = ctx
        self.sender = sender
        self.card_content = card_content
        self.select = CardSelect(
            ctx, sender=sender, recipient=recipient, card_content=card_content
        )
        self.message: Optional[discord.Message] = None
        self.add_item(self.select)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.sender.id:
            await interaction.response.send_message(
                f"I can't let you do that. Send your own cards by using `{self.ctx.clean_prefix}sendcard`"
            )
            return False
        return True

    async def on_timeout(self):
        self.select.disabled = True
        await self.message.edit(view=self)


class CardBodyModal(discord.ui.Modal):
    def __init__(
        self,
        ctx: Context,
        /,
        *,
        sender: discord.User,
        recipient: discord.User,
        card_index: int,
        card_content: Optional[str] = None,
    ):
        super().__init__(title="Compose your message", timeout=500)
        self.card_data = card_data = CARD_TYPES_DATA[card_index]
        self.recipient = recipient
        self.sender = sender
        self.ctx = ctx
        self.card_content = card_content

        self.greet = greet = discord.ui.TextInput(
            label="How to greet the recipient",
            placeholder=f'Defaults to "Dear {recipient.name},"',
            max_length=30,
            default=self.GREET_DEFAULT.format(recipient=recipient),
            required=False,
        )

        self.body = body = discord.ui.TextInput(
            label="Body of your card",
            placeholder=card_data["prompt"].format(recipient=recipient),
            max_length=1000,
            style=discord.TextStyle.long,
        )

        self.regard = regard = discord.ui.TextInput(
            label="How to send your regards",
            placeholder=f'Defaults to "From {sender.name}"',
            max_length=30,
            default=self.REGARD_DEFAULT.format(sender=sender),
            required=False,
        )

        self.add_item(greet)
        self.add_item(body)
        self.add_item(regard)

    GREET_DEFAULT = "Dear {recipient.name},"
    REGARD_DEFAULT = "From {sender.name}"

    async def on_submit(self, interaction: discord.Interaction):
        description = self.greet.value or self.GREET_DEFAULT.format(recipient=self.recipient)
        description += "\n\n" + self.body.value + "\n\n"
        description += self.regard.value or self.REGARD_DEFAULT.format(sender=self.sender)
        emoji = self.card_data["emoji"]
        embed = discord.Embed(
            title=f"{emoji} {self.card_data['name']} card {emoji}",
            description=description,
            colour=self.card_data["colour"],
        )
        await OpenCardButtonView(
            embed, sender=self.sender, recipient=self.recipient, card_content=self.card_content
        ).start_from_interaction(self.ctx, interaction)


class OpenCardButton(discord.ui.Button):
    def __init__(self, ctx: Context, card_embed: discord.Embed, /):
        super().__init__(
            style=discord.ButtonStyle.green,
            label="Open card",
            custom_id="sendcards:OpenCardButton",
            emoji="\U0001f4e9",
        )
        self.card_embed = card_embed
        self.ctx = ctx
        self.message: Optional[discord.Message] = None
        self.view: OpenCardButtonView

    async def callback(self, interaction: discord.Interaction):
        if self.label == "Open card":
            self.label = "Close card"
            self.style = discord.ButtonStyle.red
            self.emoji = "\U00002709\U0000fe0f"
            embed = self.card_embed
        else:
            self.label = "Open card"
            self.style = discord.ButtonStyle.green
            self.emoji = "\U0001f4e9"
            embed = await self.view.get_card_front_embed(self.ctx)
        await interaction.response.edit_message(embed=embed, view=self.view)


class OpenCardButtonView(discord.ui.View):
    def __init__(
        self,
        card_embed: discord.Embed,
        /,
        *,
        sender: discord.User,
        recipient: discord.User,
        card_content: Optional[str] = None,
    ):
        super().__init__(timeout=None)
        self.card_embed = card_embed
        self.sender = sender
        self.recipient = recipient
        self.card_content = card_content

    async def get_card_front_embed(self, ctx: Context):
        embed = discord.Embed(
            title=f"\U0001f4e8 You have received a card!",
            description="Interact with the button below to open it.",
            color=await ctx.embed_colour(),
        )

        if self.card_content:
            embed.add_field(
                name="In response to your card:",
                value=quote(self.card_content),
            )
        embed.set_author(
            name=self.sender.name,
            icon_url=self.sender.avatar.url,
        )

        return embed

    async def start_from_interaction(self, ctx: Context, interaction: discord.Interaction):
        self.add_item(OpenCardButton(ctx, self.card_embed))
        self.add_item(
            ReplyButton(
                ctx,
                recipient=self.recipient,
                original_sender=self.sender,
                card_content=self.card_embed.description,
            )
        )
        embed = await self.get_card_front_embed(ctx)
        try:
            await self.recipient.send(embed=embed, view=self)
        except discord.HTTPException:
            await interaction.response.send_message(
                f"Sorry, I cannot send your card. {self.recipient.name} is not currently accepting DMs from me.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"\U0001f4e8 Sent! Make sure that you allow DM messages from me, for the recipient may want to send a card back.",
                ephemeral=True,
            )


class ReplyButton(discord.ui.Button):
    def __init__(
        self,
        ctx: Context,
        *,
        recipient: discord.User,
        original_sender: discord.User,
        card_content: Optional[str] = None,
    ):
        super().__init__(
            style=discord.ButtonStyle.blurple,
            label="Send a card back",
            custom_id="sendcards:ReplyButton",
            emoji="\U0001f4dd",
        )
        self.ctx = ctx
        self.recipient = recipient
        self.original_sender = original_sender
        self.card_content = card_content

    async def callback(self, interaction: discord.Interaction):
        view = CardSelectView(
            self.ctx,
            sender=self.recipient,
            recipient=self.original_sender,
            card_content=self.card_content,
        )
        await interaction.response.send_message(view=view)
        view.message = await interaction.original_response()


class SendCards(commands.Cog):
    """Send cards to other users! (Christmas, birthday, get well soon, etc...)"""

    def __init__(self, bot: Red):
        self.bot = bot

    __author__ = "Kreusada"
    __version__ = "1.0.1"

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        return

    @commands.group(invoke_without_command=True)
    async def sendcard(self, ctx: commands.Context, user: discord.User):
        """Send a card to a user.

        The bot must share a server with the recipient. Provide
        a user ID, mention, or username. The command will ask you further questions
        in order to get information for the card.
        """
        view = CardSelectView(ctx, sender=ctx.author, recipient=user)
        view.message = await ctx.send(view=view)

    @sendcard.command()
    async def types(self, ctx: commands.Context):
        """List all the different card types."""
        await ctx.maybe_send_embed("\n".join(f"{c['emoji']} {c['name']}" for c in CARD_TYPES_DATA))
