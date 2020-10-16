import logging
import hashlib
import asyncio
import contextlib
import datetime
import discord
import itertools

from redbot.core import commands, Config, checks
from redbot.core.bot import Red
from redbot.core.config import Group
from redbot.core.i18n import Translator, cog_i18n
from redbot.core.commands import Context, Cog

T_ = Translator("Birthdays", __file__)  # pygettext3 -Dnp locales birthdays.py


def _(s):
    def func(*args, **kwargs):
        real_args = list(args)
        real_args.pop(0)
        return T_(s).format(*real_args, **kwargs)
    return func


@cog_i18n(T_)
class Birthdays(Cog):
    """Announces people's birthdays and gives them a birthday role for the whole UTC day"""
    __author__ = "ZeLarpMaster#0818"

    # Behavior related constants
    DATE_GROUP = "DATE"
    GUILD_DATE_GROUP = "GUILD_DATE"

    # Embed constants
    BDAY_LIST_TITLE = _("Birthday List")

    # Message constants
    BDAY_WITH_YEAR = _("<@!{}> is now **{} years old**. :tada:")
    BDAY_WITHOUT_YEAR = _("It's <@!{}>'s birthday today! :tada:")
    ROLE_SET = _(":white_check_mark: The birthday role on **{g}** has been set to: **{r}**.")
    BDAY_INVALID = _(":x: The birthday date you entered is invalid. It must be `MM-DD`.")
    BDAY_SET = _(":white_check_mark: Your birthday has been set to: **{}**.")
    CHANNEL_SET = _(":white_check_mark: "
                    "The channel for announcing birthdays on **{g}** has been set to: **{c}**.")
    BDAY_REMOVED = _(":put_litter_in_its_place: Your birthday has been removed.")

    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.logger = logging.getLogger("red.ZeCogsV3.birthdays")
        # force_registration is for weaklings
        unique_id = int(hashlib.sha512((self.__author__ + "@" + self.__class__.__name__).encode()).hexdigest(), 16)
        self.config = Config.get_conf(self, identifier=unique_id)
        self.config.init_custom(self.DATE_GROUP, 1)
        self.config.init_custom(self.GUILD_DATE_GROUP, 2)
        self.config.register_guild(channel=None, role=None, yesterdays=[])
        self.bday_loop = asyncio.ensure_future(self.initialise())  # Starts a loop which checks daily for birthdays
        asyncio.ensure_future(self.check_breaking_change())

    # Events
    async def initialise(self):
        await self.bot.wait_until_ready()
        with contextlib.suppress(RuntimeError):
            while self == self.bot.get_cog(self.__class__.__name__):  # Stops the loop when the cog is reloaded
                now = datetime.datetime.utcnow()
                tomorrow = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                await asyncio.sleep((tomorrow - now).total_seconds())
                await self.clean_yesterday_bdays()
                await self.do_today_bdays()

    def cog_unload(self):
        self.bday_loop.cancel()  # Forcefully cancel the loop when unloaded

    # Commands
    @commands.group()
    @commands.guild_only()
    async def bday(self, ctx: Context):
        """Birthday settings"""
        pass

    @bday.command(name="channel")
    @checks.mod_or_permissions(manage_roles=True)
    async def bday_channel(self, ctx: Context, channel: discord.TextChannel):
        """Sets the birthday announcement channel for this server"""
        message = ctx.message
        guild = message.guild
        await self.config.guild(channel.guild).channel.set(channel.id)
        await message.channel.send(self.CHANNEL_SET(g=guild.name, c=channel.name))

    @bday.command(name="role")
    @checks.mod_or_permissions(manage_roles=True)
    async def bday_role(self, ctx: Context, role: discord.Role):
        """Sets the birthday role for this server"""
        message = ctx.message
        guild = message.guild
        await self.config.guild(role.guild).role.set(role.id)
        await message.channel.send(self.ROLE_SET(g=guild.name, r=role.name))

    @bday.command(name="remove", aliases=["del", "clear", "rm"])
    async def bday_remove(self, ctx: Context):
        """Unsets your birthday date for this server"""
        message = ctx.message
        await self.remove_user_bday(message.guild.id, message.author.id)
        await message.channel.send(self.BDAY_REMOVED())

    @bday.command(name="set")
    async def bday_set(self, ctx: Context, date, year: int=None):
        """Sets your birthday date for this server
        The given date must be given as: MM-DD
        Year is optional. If ungiven, the age won't be displayed."""
        message = ctx.message
        channel = message.channel
        author = message.author
        birthday = self.parse_date(date)
        if birthday is None:
            await channel.send(self.BDAY_INVALID())
        else:
            await self.remove_user_bday(message.guild.id, author.id)
            await self.get_date_config(message.guild.id, birthday.toordinal()).get_attr(author.id).set(year)
            bday_month_str = birthday.strftime("%B")
            bday_day_str = birthday.strftime("%d").lstrip("0")  # To remove the zero-capped
            await channel.send(self.BDAY_SET(bday_month_str + " " + bday_day_str))

    @bday.command(name="list")
    async def bday_list(self, ctx: Context):
        """Lists the birthdays for this server
        If a user has their year set, it will display the age they'll get after their birthday this year"""
        message = ctx.message
        await self.clean_bdays()
        bdays = await self.get_guild_date_configs(message.guild.id)
        this_year = datetime.date.today().year
        embed = discord.Embed(title=self.BDAY_LIST_TITLE(), color=discord.Colour.lighter_grey())
        for k, g in itertools.groupby(sorted(datetime.datetime.fromordinal(int(o)) for o in bdays.keys()),
                                      lambda i: i.month):
            # Basically separates days with "\n" and people on the same day with ", "
            value = "\n".join(date.strftime("%d").lstrip("0") + ": "
                              + ", ".join("<@!{}>".format(u_id)
                                          + ("" if year is None else " ({})".format(this_year - int(year)))
                                          for u_id, year in bdays.get(str(date.toordinal()), {}).items())
                              for date in g if len(bdays.get(str(date.toordinal()))) > 0)
            if not value.isspace():  # Only contains whitespace when there's no birthdays in that month
                embed.add_field(name=datetime.datetime(year=1, month=k, day=1).strftime("%B"), value=value)
        await message.channel.send(embed=embed)

    # Utilities
    async def clean_bday(self, guild_id: int, guild_config: dict, user_id: int):
        guild = self.bot.get_guild(guild_id)
        if guild is not None:
            role = discord.utils.get(guild.roles, id=guild_config.get("role"))
            # If discord.Server.roles was an OrderedDict instead...
            await self.maybe_update_guild(guild)
            member = guild.get_member(user_id)
            if member is not None and role is not None and role in member.roles:
                # If the user and the role are still on the server and the user has the bday role
                await member.remove_roles(role)

    async def handle_bday(self, guild_id: int, user_id: int, year: str):
        embed = discord.Embed(color=discord.Colour.gold())
        if year is not None:
            age = datetime.date.today().year - int(year)  # Doesn't support non-eastern age counts but whatever
            embed.description = self.BDAY_WITH_YEAR(user_id, age)
        else:
            embed.description = self.BDAY_WITHOUT_YEAR(user_id)
        guild = self.bot.get_guild(guild_id)
        if guild is not None:  # Ignore unavailable servers or servers the bot isn't in anymore
            member = guild.get_member(user_id)
            if member is not None:
                role_id = await self.config.guild(guild).role()
                if role_id is not None:
                    role = discord.utils.get(guild.roles, id=role_id)
                    if role is not None:
                        try:
                            await member.add_roles(role)
                        except (discord.Forbidden, discord.HTTPException):
                            pass
                        else:
                            async with self.config.guild(guild).yesterdays() as yesterdays:
                                yesterdays.append(member.id)
                    else:
                        self.logger.warning("Could not find the role with id {} in {}".format(role_id, guild))
                channel_id = await self.config.guild(guild).channel()
                channel = guild.get_channel(channel_id)
                if channel is not None:
                    await channel.send(embed=embed)
                else:
                    self.logger.warning("Couldn't find the birthdays channel in guild {} with id {}".format(guild, channel_id))
            else:
                self.logger.warning("Could not find the member with id {} in {}".format(user_id, guild))
        else:
            self.logger.warning("Could not find the guild with id {}".format(guild_id))

    async def clean_bdays(self):
        # Cleans the birthday entries with no user's birthday
        # Also removes birthdays of users who aren't in any visible server anymore
        # Happens when someone changes their birthday and there's nobody else in the same day
        birthdays = await self.get_all_date_configs()
        for guild_id, guild_bdays in birthdays.items():
            for date, bdays in guild_bdays.items():
                for user_id, year in bdays.items():
                    if not any(g.get_member(int(user_id)) is not None for g in self.bot.guilds):
                        async with self.get_date_config(guild_id, date)() as config_bdays:
                            del config_bdays[user_id]
                config_bdays = await self.get_date_config(guild_id, date)()
                if len(config_bdays) == 0:
                    await self.get_date_config(guild_id, date).clear()

    async def remove_user_bday(self, guild_id: int, user_id: int):
        user_id = str(user_id)
        birthdays = await self.get_guild_date_configs(guild_id)
        for date, user_ids in birthdays.items():
            if user_id in user_ids:
                await self.get_date_config(guild_id, date).get_attr(user_id).clear()
        # Won't prevent the cleaning problem here cause the users can leave so we'd still want to clean anyway

    async def clean_yesterday_bdays(self):
        all_guild_configs = await self.config.all_guilds()
        for guild_id, guild_config in all_guild_configs.items():
            for user_id in guild_config.get("yesterdays", []):
                asyncio.ensure_future(self.clean_bday(guild_id, guild_config, user_id))
            await self.config.guild(discord.Guild(data={"id": guild_id}, state=None)).yesterdays.clear()

    async def do_today_bdays(self):
        bday_configs = await self.get_all_date_configs()
        for guild_id, bdays_config in bday_configs.items():
            this_date = datetime.datetime.utcnow().date().replace(year=1)
            todays_bday_config = bdays_config.get(str(this_date.toordinal()), {})
            for user_id, year in todays_bday_config.items():
                asyncio.ensure_future(self.handle_bday(int(guild_id), int(user_id), year))

    # Provided by <@78631113035100160>
    async def maybe_update_guild(self, guild: discord.Guild):
        # ctx.guild.chunked is innaccurate, discord.py#1638
        if not guild.unavailable and guild.large:
            if not guild.chunked or any(m.joined_at is None for m in guild.members):
                await self.bot.request_offline_members(guild)

    def parse_date(self, date_str: str):
        result = None
        try:
            result = datetime.datetime.strptime(date_str, "%m-%d").date().replace(year=1)
        except ValueError:
            pass
        return result

    async def check_breaking_change(self):
        await self.bot.wait_until_ready()
        previous = await self.config.custom(self.DATE_GROUP).all()
        if len(previous) > 0:  # Breaking change detected!
            await self.config.custom(self.DATE_GROUP).clear()
            owner = self.bot.get_user(self.bot.owner_id)
            if len(self.bot.guilds) == 1:
                await self.get_guild_date_config(self.bot.guilds[0].id).set_raw(value=previous)
                self.logger.info("Birthdays are now per-guild. Previous birthdays have been copied.")
            else:
                await self.config.custom(self.GUILD_DATE_GROUP, "backup").set_raw(value=previous)
                self.logger.info("Previous birthdays have been backed up in the config file.")
                await owner.send(""""Hey there, \
I wanted to inform you about a breaking change in this update which removed all of your users' birthday date and year. \
This means all of your users will need to add their birthday again.
For more information on why this happened, see: <https://github.com/ZeLarpMaster/ZeCogsV3/issues/15>.
I'm sorry this had to happen, but this was the best I could do to avoid mishaps.
Note: This warning should appear only once.
    - Birthdays' developer""")

    # Utilities - Config
    def get_date_config(self, guild_id: int, date: int) -> Group:
        return self.config.custom(self.GUILD_DATE_GROUP, str(guild_id), str(date))

    def get_guild_date_config(self, guild_id: int) -> Group:
        return self.config.custom(self.GUILD_DATE_GROUP, str(guild_id))

    async def get_guild_date_configs(self, guild_id: int) -> dict:
        return await self.get_guild_date_config(guild_id).all()

    async def get_all_date_configs(self) -> dict:
        return await self.config.custom(self.GUILD_DATE_GROUP).all()