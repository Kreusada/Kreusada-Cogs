import discord
from redbot.core import Config, commands
from redbot.core.bot import Red


class VoiceNick(commands.Cog):
    """Configure a nickname and role for a bot in a VC."""
    def __init__(self, bot: Red):
        self.config = Config.get_conf(self, identifier=202005118)
        self.currently_checking = []
        self.bot = bot
        default_guild = {
            "hoist_role": None
        }
        self.config.register_guild(**default_guild)

    async def red_delete_data_for_user(self, **kwargs):
        """
        Nothing to delete
        """
        return

    @commands.command(name="voicenickrole", aliases=["vnr"], help="Set a role to be given when a bot joins a voice.")
    @commands.has_permissions(administrator=True)
    async def _hoisted_role(self, ctx, role: discord.Role=None):
        data = await self.config.guild(ctx.guild).hoist_role()
        if not role:
            if not data:
                await ctx.send(f"Use `{ctx.prefix}vnr @role` to set a role.")
            else:
                await self.config.guild(ctx.guild).hoist_role.set(None)
                await ctx.send(f"Voice nick role was reset.")
        else:
            if data == role.id:
                await ctx.send(f"{role.mention} is already set as voice nick role.")
            else:
                await self.config.guild(ctx.guild).hoist_role.set(role.id)
                await ctx.send(f"{role.mention} was set as voice nick role.")

    @commands.Cog.listener("on_voice_state_update")
    async def voicenick_handler(self, member, before, after):
        if not member.bot:
            return
        data = await self.config.guild(member.guild).hoist_role()
        if before.channel == None and after.channel != None:
            try:
                if not member.nick:
                    await member.edit(nick="!" + member.name)
                if member.nick and "!" not in member.nick:
                    await member.edit(nick="!" + member.nick)
                role = member.guild.get_role(data)
                if role and role not in member.roles:
                    await member.add_roles(role)
            except:
                pass
        if before.channel != None and after.channel == None:
            try:
                if not member.nick and "!" in member.name:
                    await member.edit(nick=member.name.replace("!",""))
                if member.nick and "!" in member.nick:
                    await member.edit(nick=member.nick.replace("!", ""))
                role = member.guild.get_role(data)
                if role and role in member.roles:
                    await member.remove_roles(role)
            except:
                pass
