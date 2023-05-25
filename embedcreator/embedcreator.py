from __future__ import annotations

import discord
import json
from copy import deepcopy
from discord import Embed
from typing import Any, Optional

from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands import BadArgument, ColourConverter, Context

from redbot.core.utils.chat_formatting import bold, box, text_to_file

JSON_EMOJI = discord.PartialEmoji(name="json", animated=False, id=1110250547254141049)
REDO_EMOJI = discord.PartialEmoji(name="redo", animated=False, id=1110607817859145768)


DEFAULT_EMBED_TITLE = "Welcome to the embed builder"

DEFAULT_EMBED_DESCRIPTION = """
- Use the grey buttons to edit the various components of the embed.
- You can add or remove fields with the green and red buttons located just under the grey buttons.
- Get the embed's JSON via the "Get JSON" button. This can be used to store your embeds for shorthand, or to use elsewhere.
- There are two "Upload JSON" buttons:
    - **replace** - Replaces all the embed's current JSON data with the uploaded data.
  - **update** - Replaces only the specified keys.
- You can remove all buttons by using the "Prune buttons" button (this is done automatically after 180 seconds of inactivity).
""".strip()


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
            if self.replace:
                new = {"type": "rich", **data}
            else:
                new = embed.to_dict()
                new.update(data)
            self.view.embed = Embed.from_dict(new)


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


class EmbedFieldRemover(ModalBase):
    def __init__(self, view: EmbedEditorView):
        super().__init__(view, title="Field remover")

        self.embed_field_name = discord.ui.TextInput(
            label="Name",
            style=discord.TextStyle.short,
            placeholder="The name of the field name to remove.",
            max_length=256,
        )

    async def edit_embed(self, embed: Embed):
        x = 0
        for index, field in enumerate(embed.fields):
            if field.name == self.embed_field_name.value:
                embed.remove_field(index - x)
                x += 1

class EmbedSenderModal(SingularEmbedComponentModal):
    def __init__(self, view: EmbedEditorView):
        super().__init__(
            view,
            title="Send your embed",
            label="Channel (ID or name)",
            style=discord.TextStyle.short,
            placeholder="#" + view.context.channel.name,
        )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            location = await commands.TextChannelConverter().convert(self.view.context, self.component.value)
        except BadArgument:
            return interaction.response.send_message(
                f"Could not convert {self.component.value!r} to a valid text channel.",
                ephemeral=True,
            )
        else:
            if not all(
                [
                    location.permissions_for(self.view.context.me).send_messages,
                    location.permissions_for(self.view.context.author).send_messages,
                ]
            ):
                return interaction.response.send_message(
                    f"Both you and I must have permissions to post in {location.mention}.",
                    ephemeral=True,
                )
            try:
                await location.send(content=self.view.content, embed=self.view.embed)
            except discord.HTTPException:
                return interaction.response.send_message(
                    f"Something went wrong when trying to send this embed.",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(f"Embed sent to {location.mention}!", ephemeral=True)


class EmbedEditorView(discord.ui.View):

    content: Optional[str] = None
    message: Optional[discord.Message] = None

    def __init__(self, ctx: Context):
        self.context = ctx
        super().__init__(timeout=180)
        self.embed = discord.Embed(
            title=DEFAULT_EMBED_TITLE,
            description=DEFAULT_EMBED_DESCRIPTION,
            colour=discord.Colour.greyple(),
        )
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

    @discord.ui.button(label="Image", row=1, style=discord.ButtonStyle.grey)
    async def edit_image_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EmbedImageModal(self))

    @discord.ui.button(label="Thumbnail", row=1, style=discord.ButtonStyle.grey)
    async def edit_thumbnail_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(EmbedThumbnailModal(self))

    @discord.ui.button(label="URL", row=1, style=discord.ButtonStyle.grey)
    async def edit_url_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EmbedURLModal(self))

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
        await interaction.response.send_modal(EmbedFieldRemover(self))

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

    @discord.ui.button(label="Get JSON", style=discord.ButtonStyle.blurple, emoji=JSON_EMOJI, row=3)
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
        label="Upload JSON (replace)",
        style=discord.ButtonStyle.blurple,
        emoji=JSON_EMOJI,
        row=3,
    )
    async def upload_json_replace(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(EmbedDictionaryUpdater(self, replace=True))

    @discord.ui.button(
        label="Upload JSON (update)",
        style=discord.ButtonStyle.blurple,
        emoji=JSON_EMOJI,
        row=3,
    )
    async def upload_json_update(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_modal(EmbedDictionaryUpdater(self, replace=False))

    @discord.ui.button(
        label="Send", style=discord.ButtonStyle.green, emoji="\U0001f4e4", row=4
    )
    async def send(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EmbedSenderModal(self))

    @discord.ui.button(
        label="Prune buttons", style=discord.ButtonStyle.red, emoji="\U00002716", row=4
    )
    async def prune_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.prune_buttons()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(
        label="Delete message", style=discord.ButtonStyle.red, emoji="\U00002716", row=4
    )
    async def delete_message(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()
        await interaction.response.defer()

    async def on_timeout(self):
        await self.prune_buttons()
        await self.message.edit(view=self)

    async def prune_buttons(self):
        for item in self.children:
            self.remove_item(item)

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
                f"An error occured whilst making modifications to the embed:\n{box(exc)}\n"
            )
            self.embed = previous_embed
        else:
            await interaction.response.defer()

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.context.author:
            await interaction.response.send_message(
                "You cannot interact with the creation of this embed.",
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
    async def embedcreate(self, ctx: commands.Context, embed_message: Optional[discord.Message] = None):
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
