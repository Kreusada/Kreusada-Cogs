from __future__ import annotations

import discord
import contextlib
import json
from copy import deepcopy
from discord import Embed
from typing import Any, Optional

from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands import BadArgument, ColourConverter, Context

from redbot.core.utils.chat_formatting import bold, box, text_to_file

JSON_EMOJI = discord.PartialEmoji(name="json", animated=False, id=1110250547254141049)

DEFAULT_EMBED_TITLE = "Welcome to the embed builder"

DEFAULT_EMBED_DESCRIPTION = """
- Use the grey buttons to edit the various components of the embed. Use the red clear button to nullify all of the embed's components.
- You can add or remove fields with the green and red buttons located just under the grey buttons.
- Get the embed's Python code using the "Get Python" code. This can be used for debugs or for your own code.
- Get the embed's JSON via the "Get JSON" button. This can be used to store your embeds for shorthand, or to use elsewhere.
- There are two buttons which can modify the embed using JSON:
    - **replace** - Replaces all the embed's current JSON data with the uploaded data.
  - **update** - Replaces only the specified keys.
- Once you're done, use the "Send" dropdown to export your embed to your desired channel.
""".strip()


def shorten_by(s: str, /, length: int) -> str:
    if len(s) > length:
        return s[: length - 1] + "…"
    return s


class ModalBase(discord.ui.Modal):
    def __init__(
        self,
        view: EmbedEditorView,
        /,
        *,
        title: str,
    ):
        self.view = view
        super().__init__(title=title)

    def __setattr__(self, name: str, value: Any):
        if isinstance(value, discord.ui.TextInput):
            self.add_item(value)
        super().__setattr__(name, value)

    async def edit_embed(self, embed: discord.Embed):
        pass

    async def on_submit(self, interaction: discord.Interaction):
        await self.view.modify_embed(self, interaction)


class SingularEmbedComponentModal(ModalBase):
    def __init__(
        self,
        view: EmbedEditorView,
        /,
        *,
        title: str,
        label: str,
        style: discord.TextStyle = discord.TextStyle.short,
        placeholder: Optional[str] = None,
        default: Optional[str] = None,
        required: bool = True,
        max_length: Optional[int] = None,
    ):
        super().__init__(view, title=title)

        self.component = discord.ui.TextInput(
            label=label,
            style=style,
            placeholder=placeholder,
            default=default,
            required=required,
            max_length=max_length,
        )


class EmbedTitleModal(SingularEmbedComponentModal):
    def __init__(self, view: EmbedEditorView):
        super().__init__(
            view,
            title="Set embed title",
            label="Text for the embed title",
            style=discord.TextStyle.short,
            default=view.embed.title,
            required=False,
            max_length=256,
        )

    async def edit_embed(self, embed: Embed):
        embed.title = self.component.value or None


class EmbedDescriptionModal(SingularEmbedComponentModal):
    def __init__(self, view: EmbedEditorView):
        super().__init__(
            view,
            title="Set embed description",
            label="Text for the embed description",
            style=discord.TextStyle.long,
            default=view.embed.description,
            required=False,
            max_length=4000,
        )

    async def edit_embed(self, embed: Embed):
        embed.description = self.component.value or None


class EmbedMessageContentModal(SingularEmbedComponentModal):
    def __init__(self, view: EmbedEditorView):
        super().__init__(
            view,
            title="Set message content",
            label="Text for the message content",
            style=discord.TextStyle.long,
            default=view.content,
            required=False,
            max_length=2000,
        )

    async def edit_embed(self, embed: Embed):
        self.view.content = self.component.value or None


class EmbedColourModal(SingularEmbedComponentModal):
    def __init__(self, view: EmbedEditorView, *, context: Context):
        super().__init__(
            view,
            title="Set embed colour",
            label="Enter integer, hex code, or colour name",
            style=discord.TextStyle.short,
            default=str(view.embed.colour or ""),
            required=False,
        )
        self.context = context

    async def edit_embed(self, embed: Embed):
        colour = self.component.value or None
        if colour:
            try:
                embed.colour = await ColourConverter().convert(self.context, colour)
            except BadArgument:
                raise ValueError(f"Invalid colour {colour!r}")
        else:
            embed.colour = None


class EmbedImageModal(SingularEmbedComponentModal):
    def __init__(self, view: EmbedEditorView):
        super().__init__(
            view,
            title="Set embed image",
            label="Image URL",
            style=discord.TextStyle.short,
            default=view.embed.image.url or "",
            required=False,
        )

    async def edit_embed(self, embed: Embed):
        embed.set_image(url=self.component.value or None)


class EmbedThumbnailModal(SingularEmbedComponentModal):
    def __init__(self, view: EmbedEditorView):
        super().__init__(
            view,
            title="Set embed thumbnail",
            label="Thumbnail URL",
            style=discord.TextStyle.short,
            default=view.embed.thumbnail.url or "",
            required=False,
        )

    async def edit_embed(self, embed: Embed):
        embed.set_thumbnail(url=self.component.value or None)


class EmbedURLModal(SingularEmbedComponentModal):
    def __init__(self, view: EmbedEditorView):
        super().__init__(
            view,
            title="Set embed URL",
            label="URL",
            style=discord.TextStyle.short,
            default=view.embed.url or "",
            required=False,
        )

    async def edit_embed(self, embed: Embed):
        embed.url = self.component.value or None


class EmbedDictionaryUpdater(SingularEmbedComponentModal):
    def __init__(self, view: EmbedEditorView, *, replace: bool):
        super().__init__(
            view,
            title="Upload JSON data",
            label="JSON data",
            style=discord.TextStyle.long,
            default=None,
            required=False,
        )
        self.replace = replace

    async def edit_embed(self, embed: Embed):
        try:
            data = json.loads(self.component.value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON (`{exc}`)")
        else:
            data["type"] = "rich"
            if self.replace:
                new = data
            else:
                new = embed.to_dict()
                new.update(data)
            try:
                self.view.embed = Embed.from_dict(new)
            except Exception as exc:
                raise ValueError(exc)


class EmbedFooterBuilder(ModalBase):
    def __init__(self, view: EmbedEditorView):
        super().__init__(view, title="Footer details")

        self.embed_footer_text = discord.ui.TextInput(
            label="Footer text",
            style=discord.TextStyle.long,
            max_length=2048,
            default=view.embed.footer.text,
            required=False,
        )

        self.embed_footer_icon_url = discord.ui.TextInput(
            label="Footer icon URL",
            style=discord.TextStyle.short,
            default=view.embed.footer.icon_url,
            required=False,
        )

    async def edit_embed(self, embed: Embed):
        embed.set_footer(
            text=self.embed_footer_text.value, icon_url=self.embed_footer_icon_url.value
        )


class EmbedAuthorBuilder(ModalBase):
    def __init__(self, view: EmbedEditorView):
        super().__init__(view, title="Author details")

        self.embed_author_name = discord.ui.TextInput(
            label="Author name",
            style=discord.TextStyle.short,
            max_length=256,
            default=self.view.embed.author.name,
            required=True,
        )

        self.embed_author_url = discord.ui.TextInput(
            label="Author URL",
            style=discord.TextStyle.short,
            default=self.view.embed.author.url,
            required=False,
        )

        self.embed_author_icon_url = discord.ui.TextInput(
            label="Author icon URL",
            style=discord.TextStyle.short,
            default=self.view.embed.author.icon_url,
            required=False,
        )

    async def edit_embed(self, embed: Embed):
        embed.set_author(
            name=self.embed_author_name.value,
            url=self.embed_author_url.value,
            icon_url=self.embed_author_icon_url.value,
        )


class EmbedFieldAdder(ModalBase):
    def __init__(self, view: EmbedEditorView):
        super().__init__(view, title="Field adder")

        self.embed_field_name = discord.ui.TextInput(
            label="Name",
            style=discord.TextStyle.short,
            max_length=256,
        )

        self.embed_field_value = discord.ui.TextInput(
            label="Value",
            style=discord.TextStyle.long,
            max_length=1024,
        )

        self.embed_field_inline = discord.ui.TextInput(
            label="Inline (true/false)",
            style=discord.TextStyle.short,
            max_length=5,
            default="true",
        )

    async def edit_embed(self, embed: Embed):
        inline = self.embed_field_inline.value.lower()
        if inline == "true":
            inline = True
        elif inline == "false":
            inline = False
        else:
            raise ValueError("Embed field inline must be 'true' or 'false'.")
        embed.add_field(
            name=self.embed_field_name.value,
            value=self.embed_field_value.value,
            inline=inline,
        )


class EmbedFieldRemoverSelect(discord.ui.Select):
    def __init__(self, view: EmbedEditorView, /):
        options = [
            discord.SelectOption(
                label=shorten_by(field.name, 100),
                description=shorten_by(field.value, 100),
                value=str(index),
            )
            for index, field in enumerate(view.embed.fields)
        ]
        super().__init__(placeholder="Select a field to remove", options=options)
        self.embed_editor_view = view

    async def callback(self, interaction: discord.Interaction):
        self.embed_editor_view.embed.remove_field(int(self.values[0]))
        await self.embed_editor_view.message.edit(embed=self.embed_editor_view.embed)
        await interaction.response.edit_message(
            content="Field removed.",
            view=None,
        )


class EmbedFieldRemoverView(discord.ui.View):
    def __init__(self, view: EmbedEditorView):
        super().__init__(timeout=30)
        self.add_item(EmbedFieldRemoverSelect(view))
        self.message: Optional[discord.Message] = None

    async def on_timeout(self):
        with contextlib.suppress(discord.HTTPException):
            await self.message.delete()


class EmbedEditorView(discord.ui.View):
    def __init__(self, ctx: Context):
        self.context = ctx
        super().__init__(timeout=180)
        self.embed = discord.Embed(
            title=DEFAULT_EMBED_TITLE,
            description=DEFAULT_EMBED_DESCRIPTION,
            colour=discord.Colour.greyple(),
        )
        self.embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        self.content: Optional[str] = None
        self.message: Optional[discord.Message] = None

    @discord.ui.button(label="Title", style=discord.ButtonStyle.grey)
    async def edit_title_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EmbedTitleModal(self))

    @discord.ui.button(label="Description", style=discord.ButtonStyle.grey)
    async def edit_description_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(EmbedDescriptionModal(self))

    @discord.ui.button(label="Message content", style=discord.ButtonStyle.grey)
    async def edit_message_content_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(EmbedMessageContentModal(self))

    @discord.ui.button(label="Colour", style=discord.ButtonStyle.grey)
    async def edit_colour_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(EmbedColourModal(self, context=self.context))

    @discord.ui.button(label="URL", style=discord.ButtonStyle.grey)
    async def edit_url_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EmbedURLModal(self))

    @discord.ui.button(label="Image", row=1, style=discord.ButtonStyle.grey)
    async def edit_image_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EmbedImageModal(self))

    @discord.ui.button(label="Thumbnail", row=1, style=discord.ButtonStyle.grey)
    async def edit_thumbnail_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(EmbedThumbnailModal(self))

    @discord.ui.button(label="Author", row=1, style=discord.ButtonStyle.grey)
    async def edit_author_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(EmbedAuthorBuilder(self))

    @discord.ui.button(label="Footer", row=1, style=discord.ButtonStyle.grey)
    async def edit_footer_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(EmbedFooterBuilder(self))

    @discord.ui.button(label="Clear", row=1, style=discord.ButtonStyle.red)
    async def clear_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(description="[…]")
        self.embed = embed
        self.content = None
        await interaction.response.edit_message(embed=self.embed, content=self.content)

    @discord.ui.button(
        label="Add field", style=discord.ButtonStyle.green, emoji="\U00002795", row=2
    )
    async def add_field_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EmbedFieldAdder(self))

    @discord.ui.button(
        label="Remove field", style=discord.ButtonStyle.red, emoji="\U00002796", row=2
    )
    async def remove_field_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if not self.embed.fields:
            await interaction.response.send_message(
                "There are no fields to remove.", ephemeral=True
            )
        else:
            view = EmbedFieldRemoverView(self)
            await interaction.response.send_message(view=view, ephemeral=True)
            view.message = await interaction.original_response()

    @discord.ui.button(
        label="Get Python", style=discord.ButtonStyle.blurple, emoji="\U0001f40d", row=3
    )
    async def get_python(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.embed
        text = "embed = discord.Embed("
        if embed.title:
            text += f"\n\ttitle={embed.title!r},"
        if embed.description:
            text += f"\n\tdescription={embed.description!r},"
        if embed.colour:
            text += f"\n\tcolour={int(embed.colour)},"
        if embed.url:
            text += f"\n\turl={embed.url!r},"

        if text == "embed = discord.Embed(":
            text += ")"
        else:
            text += "\n)"
        text += "\n\n"

        if embed.image:
            text += f"embed.set_image(url={embed.image.url!r})\n"
        if embed.thumbnail:
            text += f"embed.set_thumbnail(url={embed.thumbnail.url!r})\n"

        if embed.author:
            attrs = {}
            for attr in ["name", "url", "icon_url"]:
                if (gattr := getattr(embed.author, attr)) :
                    attrs[attr] = gattr
            text += (
                f"embed.set_author(" + ", ".join(f"{k}={v!r}" for k, v in attrs.items()) + ")\n"
            )

        if embed.footer:
            attrs = {}
            for attr in ["text", "icon_url"]:
                if (gattr := getattr(embed.footer, attr)) :
                    attrs[attr] = gattr
            text += (
                f"embed.set_footer(" + ", ".join(f"{k}={v!r}" for k, v in attrs.items()) + ")\n"
            )

        if not text.endswith("\n\n"):
            text += "\n"

        if embed.fields:
            for field in embed.fields:
                text += f"embed.add_field(name={field.name!r}, value={field.value!r}, inline={field.inline!r})\n"
            text += "\n\n"

        if self.content:
            text += f"content = {self.content!r}\n"

        text += "await ctx.send("
        if self.content:
            text += "content, "
        text += "embed=embed)"

        if len(text) > 1990:
            await interaction.response.send_message(
                file=text_to_file(text, filename="embed.py"),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                box(text.replace("```", "~~~"), lang="py"),
                ephemeral=True,
            )

    @discord.ui.button(
        label="Get JSON", style=discord.ButtonStyle.blurple, emoji=JSON_EMOJI, row=3
    )
    async def get_json(self, interaction: discord.Interaction, button: discord.ui.Button):
        text = json.dumps(self.embed.to_dict(), indent=4)
        if len(text) > 1990:
            await interaction.response.send_message(
                file=text_to_file(text, filename="embed.json"),
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                box(text.replace("```", "~~~"), lang="json"),
                ephemeral=True,
            )

    @discord.ui.button(
        label="Replace JSON",
        style=discord.ButtonStyle.grey,
        emoji=JSON_EMOJI,
        row=3,
    )
    async def replace_json(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EmbedDictionaryUpdater(self, replace=True))

    @discord.ui.button(
        label="Update JSON",
        style=discord.ButtonStyle.grey,
        emoji=JSON_EMOJI,
        row=3,
    )
    async def update_json(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EmbedDictionaryUpdater(self, replace=False))

    @discord.ui.select(
        cls=discord.ui.ChannelSelect,
        channel_types=[
            discord.ChannelType.text,
            discord.ChannelType.news,
            discord.ChannelType.news_thread,
            discord.ChannelType.public_thread,
            discord.ChannelType.private_thread,
            discord.ChannelType.forum,
        ],
        placeholder="Send your embed",
        row=4,
    )
    async def send(self, interaction: discord.Interaction, select: discord.ui.ChannelSelect):
        channel = interaction.guild.get_channel(select.values[0].id)
        if not channel.permissions_for(interaction.guild.me).send_messages:
            return await interaction.response.send_message(
                f"I do not have permissions to post in {channel.mention}.", ephemeral=True
            )
        try:
            await channel.send(embed=self.embed, content=self.content)
        except discord.HTTPException:
            return await interaction.response.send_message(
                "Something went wrong whilst sending the embed."
            )
        else:
            await interaction.response.send_message(
                f"Embed sent to {channel.mention}.", ephemeral=True
            )

    async def on_timeout(self):
        await self.message.edit(view=None)

    async def modify_embed(self, modal: ModalBase, interaction: discord.Interaction):
        previous_embed = deepcopy(self.embed)
        try:
            await modal.edit_embed(self.embed)
        except ValueError as exc:
            return await interaction.response.send_message(f"An error occured: {exc}")
        try:
            await interaction.message.edit(embed=self.embed, content=self.content)
        except discord.HTTPException as exc:
            exc = exc.text.replace("embeds.0.", "embed ")
            if "maximum size of 6000" in exc:
                return await interaction.response.send_message(
                    "Sorry, the embed limit has exceeded 6000 characters, which is the maximum size. Your change could not be made.",
                    ephemeral=True,
                )
            await interaction.response.send_message(
                f"A HTTP error occured whilst making modifications to the embed:\n{box(exc)}\n"
            )
            self.embed = previous_embed
        else:
            await interaction.response.defer()

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.context.author:
            await interaction.response.send_message(
                "You cannot interact with this embed.",
                ephemeral=True,
            )
            return False
        return True


class EmbedCreator(commands.Cog):
    """Create embeds using buttons and modals!"""

    __author__ = "Kreusada"
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot

    def format_help_for_context(self, ctx: commands.Context) -> str:
        context = super().format_help_for_context(ctx)
        return f"{context}\n\nAuthor: {self.__author__}\nVersion: {self.__version__}"

    async def red_delete_data_for_user(self, **kwargs):
        return

    @commands.command(aliases=["ecreate"])
    @commands.mod()
    async def embedcreate(
        self, ctx: commands.Context, embed_message: Optional[discord.Message] = None
    ):
        """Create an embed.

        `embed_message` can be the ID or URL to a message that contains an embed.
        If supplied, the embed creator will use the message's first embed as the opening template.
        """
        view = EmbedEditorView(ctx)
        embed = (
            deepcopy(embed_message.embeds[0])
            if embed_message and embed_message.embeds
            else view.embed
        )
        view.embed = embed
        view.message = await ctx.send(view=view, embed=embed)
