import discord
from typing import Optional
from datetime import datetime
from redbot.core import commands, checks, Config, modlog


class Getroles(commands.Cog):
    """Getroles"""

    def __init__(self):
        self.config = Config.get_conf(self, 200730042020, force_registration=True)

    @commands.group()
    @checks.admin()
    async def getroles(self, ctx):
        """All getrole settings."""
        pass

    @getroles.command()
    async def test(self, ctx):
        """This is a test category."""
        await ctx.send(f"Testing.")

#    @getroles.command()
#    async def testrole(
#        self, ctx: commands.Context, member: discord.Member, role: discord.Role, *, check_user=True
#    ):
#        if role in member.roles:
#            await ctx.send(
#                _("{member.display_name} already has the role {role.name}.").format(
#                    role=role, member=member
#                )
            
#    @getroles.command()
#    @commands.guild_only()
#    @checks.admin_or_permissions(manage_roles=True)
#    async def testrole(
#        self, ctx: commands.Context, rolename: discord.Role, *, user: discord.Member = None
#    ):
#        if user is None:
#            user = ctx.author
#        await self._getroles(ctx, user, rolename)
#        
#    @commands.guild_only()
#    @commands.group()
#    async def selfrole(self, ctx: commands.Context):
#        """Apply selfroles."""
#        pass
#
#    @getroles.command()
#    async def testselfrole(self, ctx: commands.Context, *, testselfrole: getroles):
#        """
#        Add a selfrole to yourself.
#        Server admins must have configured the role as user settable.
#        NOTE: The role is case sensitive!
#        """
#        # noinspection PyTypeChecker
#        await self._addrole(ctx, ctx.author, testselfrole, check_user=False)
#
#    @ticketer.group()
#    async def category(self, ctx):
#        """Set the categories for open and closed tickets."""
#
#    @category.group()
#    async def open(self, ctx, *, category: discord.CategoryChannel):
#        """Set the category for open tickets."""
#        await self.config.guild(ctx.guild).open_category.set(category.id)
#        await ctx.send(f"Category for open tickets has been set to {category.mention}")
#
#    @category.group()
#    async def closed(self, ctx, *, category: discord.CategoryChannel):
#        """Set the category for open tickets."""
#        await self.config.guild(ctx.guild).closed_category.set(category.id)
#        await ctx.send(f"Category for closed tickets has been set to {category.mention}")
#
#    @ticketer.command()
#    async def message(self, ctx, *, message: str):
#        """Set the message that is shown at the start of each ticket channel."""
#        await self.config.guild(ctx.guild).message.set(message)
#        await ctx.send(f"The message has been set to ``{message}``.")
#
#    @ticketer.command()
#    async def counter(self, ctx, true_or_false: bool):
#        """Toggle if the ticket channels should be named using a user's name and ID or counting upwards starting at 0."""
#        await self.config.guild(ctx.guild).use_counter.set(true_or_false)
#        await ctx.send(
#            "The counter has been {}.".format("enabled. Ticket channel names will now be named as `ticket-<number>`" if true_or_false else "disabled. Ticket channel names will be named as `ticket-<user><user ID>`")
#        )
#
#    @ticketer.command()
#    async def modlog(self, ctx, true_or_false: bool):
#        """Decide if ticketer should log to modlog."""
#        await self.config.guild(ctx.guild).modlog.set(true_or_false)
#        await ctx.send(
#            "Logging to modlog has been {}.".format("enabled" if true_or_false else "disabled")
#        )
#
#    @ticketer.command()
#    async def purge(self, ctx, are_you_sure: Optional[bool]):
#        """Deletes all closed ticket channels."""
#        if are_you_sure:
#            async with self.config.guild(ctx.guild).closed() as closed:
#                for channel in closed:
#                    try:
#                        channel_obj = ctx.guild.get_channel(channel)
#                        if channel_obj:
#                            await channel_obj.delete(reason="Ticket purge")
#                        closed.remove(channel)
#                    except discord.Forbidden:
#                        await ctx.send(
#                            f"I could not delete channel ID {channel} because I don't have the required permissions."
#                        )
#                    except discord.NotFound:
#                        closed.remove(channel)
#                    except discord.HTTPException:
#                        await ctx.send("Something went wrong. Aborting.")
#                        return
#        else:
#            await ctx.send(
#                f"This action will permanently delete all closed ticket channels.\nThis action is irreversible.\nConfirm with ``{ctx.clean_prefix}ticketer purge true``"
#            )
#    @ticketer.command()
#    async def help(self, ctx):
#        """Provides a support menu for ticketer setup."""
#        await ctx.send('You can read our `ticketer` documentation here, which will show you how to use this cog: https://kreusadacogs.readthedocs.io/en/latest/tickets.html#tickets\nThe documentation was scripted by **Kreusada**. You can also join our support server here: https://discord.gg/JmCFyq7')
#
#    @commands.group()
#    async def ticket(self, ctx):
#        """Manage a ticket."""
#        pass
#
#    @ticket.command(aliases=["open"])
#    async def create(
#        self,
#        ctx,
#        *,
#        reason: Optional[str] = "No reason provided.",
#    ):
#        """Create a ticket."""
#        if await self._check_settings(ctx):
#            settings = await self.config.guild(ctx.guild).all()
#            if settings["use_counter"]:
#                name = f"ticket-{settings['current_ticket']}"
#                await self.config.guild(ctx.guild).current_ticket.set(
#                    settings["current_ticket"] + 1
#                )
#            else:
#                name = f"{ctx.author.name}-{ctx.author.id}"
#            found = False
#            for channel in ctx.guild.channels:
#                if channel.name == name.lower():
#                    found = True
#            if not found:
#                if settings["modlog"]:
#                    await modlog.create_case(
#                        ctx.bot,
#                        ctx.guild,
#                        ctx.message.created_at,
#                        action_type="ticket_created",
#                        user=ctx.author,
#                        moderator=ctx.author,
#                        reason=reason,
#                    )
#                overwrite = {
#                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
#                    ctx.author: discord.PermissionOverwrite(
#                        read_messages=True,
#                        send_messages=True,
#                        embed_links=True,
#                        attach_files=True,
#                    ),
#                    ctx.guild.get_role(settings["role"]): discord.PermissionOverwrite(
#                        read_messages=True,
#                        send_messages=True,
#                        embed_links=True,
#                        attach_files=True,
#                        manage_messages=True,
#                    ),
#                }
#                ticketchannel = await ctx.guild.create_text_channel(
#                    name,
#                    overwrites=overwrite,
#                    category=ctx.guild.get_channel(settings["open_category"]),
#                    topic=reason,
#                )
#                await ticketchannel.send(settings["message"])
#                embed = discord.Embed(
#                    title=name,
#                    description=reason,
#                    timestamp=datetime.utcnow(),
#                ).set_footer(text="Last updated at:")
#                message = await ctx.guild.get_channel(settings["channel"]).send(embed=embed)
#                async with self.config.guild(ctx.guild).active() as active:
#                    active.append((ticketchannel.id, message.id))
#            else:
#                await ctx.send("You already have an open ticket! You can close it in your ticket channel by using `,ticketclose`.")
#        else:
#            await ctx.send("Please finish the setup process before creating a ticket.")
#
#    @ticket.command()
#    async def close(self, ctx):
#        """Close a ticket."""
#        settings = await self.config.guild(ctx.guild).all()
#        active = settings["active"]
#        success = False
#        for ticket in active:
#            if ctx.channel.id in ticket:
#                new_embed = (
#                    await ctx.guild.get_channel(settings["channel"]).fetch_message(ticket[1])
#                ).embeds[0]
#                new_embed.add_field(
#                    name=datetime.utcnow().strftime("%H:%m UTC"),
#                    value=f"Ticket closed by {ctx.author.name}#{ctx.author.discriminator}",
#                )
#                new_embed.timestamp = datetime.utcnow()
#                await (
#                    await ctx.guild.get_channel(settings["channel"]).fetch_message(ticket[1])
#                ).edit(
#                    embed=new_embed,
#                    delete_after=10,
#                )
#                await ctx.send(embed=new_embed)
#                await ctx.send(
#                    "You can submit additional tickets by using `,ticketcreate`.", delete_after=30
#                )
#                await ctx.channel.edit(
#                    category=ctx.guild.get_channel(settings["closed_category"]),
#                    name=f"expired - {ctx.channel.name}",
#                    overwrites={
#                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
#                        ctx.guild.get_role(settings["role"]): discord.PermissionOverwrite(
#                            read_messages=True,
#                            send_messages=True,
#                            embed_links=True,
#                            attach_files=True,
#                            manage_messages=True,
#                        ),
#                    },
#                )
#                await ctx.send("Ticket closed.")
#                active.remove(ticket)
#                async with self.config.guild(ctx.guild).closed() as closed:
#                    closed.append(ticket[0])
#                success = True
#        if not success:
#            await ctx.send("This is not a ticket channel, please move to your ticket channel when running this command.")
#        await self.config.guild(ctx.guild).active.set(active)
#
#    @ticket.command()
#    @checks.mod()
#    async def update(self, ctx, ticket: Optional[discord.TextChannel] = None, *, update: str):
#        """Update a ticket. This is visible to all participants of the ticket."""
#        if ticket is None:
#            channel = ctx.channel
#        else:
#            channel = ticket
#        settings = await self.config.guild(ctx.guild).all()
#        active = settings["active"]
#        for ticket in active:
#            if channel.id in ticket:
#                await channel.edit(
#                    topic=f'{channel.topic}\n\n{ctx.author.name}#{ctx.author.discriminator}:"{update}"'
#                )
#                await ctx.send("Ticket updated.", delete_after=10)
#            else:
#                ctx.send(f"{channel.mention} is not a ticket channel.")
#
#    @ticket.command()
#    @checks.mod()
#    async def note(self, ctx, ticket: discord.TextChannel, *, note: str):
#        """Add a staff-only note to a ticket."""
#        channel = ticket
#        for ticket in await self.config.guild(ctx.guild).active():
#            if channel.id in ticket:
#                message = await ctx.guild.get_channel(
#                    await self.config.guild(ctx.guild).channel()
#                ).fetch_message(ticket[1])
#                new_embed = message.embeds[0]
#                new_embed.add_field(
#                    name=f"{ctx.author.name}#{ctx.author.discriminator}", value=note
#                )
#                new_embed.timestamp = datetime.utcnow()
#                await message.edit(embed=new_embed)
#                await ctx.send("Note added.", delete_after=10)
#            else:
#                await ctx.send("This is not a ticket channel.")
#
#    async def _check_settings(self, ctx: commands.Context) -> bool:
#        settings = await self.config.guild(ctx.guild).all()
#        count = 0
#        if settings["channel"]:
#            count += 1
#        else:
#            await ctx.send("Management channel not set up yet.")
#        if settings["closed_category"]:
#            count += 1
#        else:
#            await ctx.send("Category for closed tickets not set up yet.")
#        if settings["open_category"]:
#            count += 1
#        else:
#            await ctx.send("Category for open tickets not set up yet.")
#        if settings["role"]:
#            count += 1
#        else:
#            await ctx.send("Ticket manager role not set up yet.")
#        if count == 4:
#            return True
#        else:
#            return False
#
