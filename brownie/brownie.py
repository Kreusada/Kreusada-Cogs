# Reviewing V2-V3 Translation for Brownie
import asyncio
import os
import random
import time
from operator import itemgetter

# Discord and Red
import discord
from .utils import checks
from __main__ import send_cmd_help
from .utils.dataIO import dataIO
from discord.ext import commands


class PluralDict(dict):
    """This class is used to plural strings
    You can plural strings based on the value input when using this class as a dictionary.
    """
    def __missing__(self, key):
        if '(' in key and key.endswith(')'):
            key, rest = key.split('(', 1)
            value = super().__getitem__(key)
            suffix = rest.rstrip(')').split(',')
            if len(suffix) == 1:
                suffix.insert(0, '')
            return suffix[0] if value <= 1 else suffix[1]
        raise KeyError(key)


class Brownie:
    """Collector loves brownies, and will steal from others for you!"""

    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/brownie/brownie.json"
        self.system = dataIO.load_json(self.file_path)

    @commands.group(pass_context=True, no_pm=True)
    async def setbrownie(self, ctx):
        """brownie settings group command"""

        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @setbrownie.command(name="stealcd", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _stealcd_heist(self, ctx, cooldown: int):
        """Set the cooldown for stealing brownies"""
        server = ctx.message.server
        settings = self.check_server_settings(server)
        if cooldown >= 0:
            settings["Config"]["Steal CD"] = cooldown
            dataIO.save_json(self.file_path, self.system)
            msg = "Cooldown for steal set to {}".format(cooldown)
        else:
            msg = "Cooldown needs to be higher than 0."
        await self.bot.say(msg)

    @setbrownie.command(name="browniecd", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _browniecd_heist(self, ctx, cooldown: int):
        """Set the cooldown for brownie command"""
        server = ctx.message.server
        settings = self.check_server_settings(server)
        if cooldown >= 0:
            settings["Config"]["brownie CD"] = cooldown
            dataIO.save_json(self.file_path, self.system)
            msg = "Cooldown for brownie set to {}".format(cooldown)
        else:
            msg = "Cooldown needs to be higher than 0."
        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True, aliases=['giveb',])
    async def givebrownie(self, ctx, user: discord.Member, brownies: int):
        """Gives another user your brownies"""
        author = ctx.message.author
        settings = self.check_server_settings(author.server)
        if user.bot:
            return await self.bot.say("I do not accept brownies from strangers.")
        if author.id == user.id:
            return await self.bot.say("You can't give yourself brownie points.")
        self.account_check(settings, author)
        self.account_check(settings, user)
        sender_brownies = settings["Players"][author.id]["brownies"]
        if 0 < brownies <= sender_brownies:
            settings["Players"][author.id]["brownies"] -= brownies
            settings["Players"][user.id]["brownies"] += brownies
            dataIO.save_json(self.file_path, self.system)
            msg = "{} gave {} brownies to {}".format(author.name, brownies, user.name)
        else:
            msg = "You don't have enough brownies points"
        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    async def nom(self,ctx):
        '''Eat a brownie'''
        author=ctx.message.author
        settings=self.check_server_settings(author.server)
        self.account_check(settings, author)
        brownies = settings['Players'][author.id]['brownies']
        if brownies == 0:
            await self.bot.say('There are no brownies to eat.')
        elif brownies >= 0:
            brownies = brownies - 1
            settings['Players'][author.id]['brownies'] = brownies
            dataIO.save_json(self.file_path, self.system)
            if brownies > 1:
                await self.bot.say('Nom nom nom.\n{} has {} brownie points remaining.'.format(author.name, brownies))
            elif brownies == 1:
                await self.bot.say('Nom nom nom.\n{} has 1 brownie point remaining'.format(author.name))
            else:
                await self.bot.say('Nom nom nom.\n{} has no more brownie points'.format(author.name))



    @commands.command(pass_context=True, no_pm=True)
    async def brownie(self, ctx):
        """Obtain a random number of brownies. 12h cooldown"""
        author = ctx.message.author
        server = ctx.message.server
        action = "brownie CD"
        settings = self.check_server_settings(server)
        self.account_check(settings, author)
        if await self.check_cooldowns(author.id, action, settings):
            weighted_sample = [1] * 152 + [x for x in range(49) if x > 1]
            brownies = random.choice(weighted_sample)
            settings["Players"][author.id]["brownies"] += brownies
            dataIO.save_json(self.file_path, self.system)
            if brownies > 1:
                await self.bot.say("{} found {} brownies!".format(author.name, brownies))
            else:
                await self.bot.say('{} found 1 brownie!'.format(author.name))

    @commands.command(pass_context=True, no_pm=False, ignore_extra=False)
    async def brownies(self, ctx):
        """See how many brownie points you have."""
        author = ctx.message.author
        server = ctx.message.server
        settings = self.check_server_settings(server)
        self.account_check(settings, author)
        brownies = settings["Players"][author.id]["brownies"]
        await self.bot.say('{} has **{}** brownie points.'.format(author.name, brownies))

    @commands.command(pass_context=True, no_pm=True)
    async def steal(self, ctx, user: discord.Member=None):
        """Steal brownies from another user. 2h cooldown."""
        author = ctx.message.author
        server = author.server
        action = "Steal CD"
        settings = self.check_server_settings(author.server)
        self.account_check(settings, author)

        if user is None:
            user = self.random_user(settings, author, server)

        if user == "Fail":
            pass
        elif user.bot:
            return await self.bot.say("Stealing failed because the picked target is a bot.\nYou "
                                      "can retry stealing again, your cooldown is not consumed.")

        if await self.check_cooldowns(author.id, action, settings):
            msg = self.steal_logic(settings, user, author)
            await self.bot.say("{} is on the prowl to steal brownies.".format(author.name))
            await asyncio.sleep(4)
            await self.bot.say(msg)

    async def check_cooldowns(self, userid, action, settings):
        path = settings["Config"][action]
        if abs(settings["Players"][userid][action] - int(time.perf_counter())) >= path:
            settings["Players"][userid][action] = int(time.perf_counter())
            dataIO.save_json(self.file_path, self.system)
            return True
        elif settings["Players"][userid][action] == 0:
            settings["Players"][userid][action] = int(time.perf_counter())
            dataIO.save_json(self.file_path, self.system)
            return True
        else:
            s = abs(settings["Players"][userid][action] - int(time.perf_counter()))
            seconds = abs(s - path)
            remaining = self.time_formatting(seconds)
            await self.bot.say("This action has a cooldown. You still have:\n{}".format(remaining))
            return False

    def steal_logic(self, settings, user, author):
        success_chance = random.randint(1, 100)
        if user == "Fail":
            msg = "I couldn't find anyone with brownie points."
            return msg

        if user.id not in settings["Players"]:
            self.account_check(settings, user)

        if settings["Players"][user.id]["brownies"] == 0:
            msg = ('{} has no brownie points.'.format(user.name))
        else:
            if success_chance <= 90:
                brownie_jar = settings["Players"][user.id]["brownies"]
                brownies_stolen = int(brownie_jar * 0.75)

                if brownies_stolen == 0:
                    brownies_stolen = 1

                stolen = random.randint(1, brownies_stolen)
                settings["Players"][user.id]["brownies"] -= stolen
                settings["Players"][author.id]["brownies"] += stolen
                dataIO.save_json(self.file_path, self.system)
                msg = ("{} stole {} brownie points from {}!".format(author.name, stolen, user.name))
            else:
                msg = "I could not find their brownie points."
        return msg

    def random_user(self, settings, author, server):
        filter_users = [server.get_member(x) for x in settings["Players"]
                        if hasattr(server.get_member(x), "name")]
        legit_users = [x for x in filter_users if x.id != author.id and x is not x.bot]

        users = [x for x in legit_users if settings["Players"][x.id]["brownies"] > 0]

        if not users:
            user = "Fail"
        else:
            user = random.choice(users)
            if user == user.bot:
                users.remove(user.bot)
                settings["Players"].pop(user.bot)
                dataIO.save_json(self.file_path, self.system)
                user = random.choice(users)
            self.account_check(settings, user)
        return user

    def account_check(self, settings, userobj):
        if userobj.id not in settings["Players"]:
            settings["Players"][userobj.id] = {"brownies": 0,
                                               "Steal CD": 0,
                                               "brownie CD": 0}
            dataIO.save_json(self.file_path, self.system)

    def time_formatting(self, seconds):
        # Calculate the time and input into a dict to plural the strings later.
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        data = PluralDict({'hour': h, 'minute': m, 'second': s})
        if h > 0:
            fmt = "{hour} hour{hour(s)}"
            if data["minute"] > 0 and data["second"] > 0:
                fmt += ", {minute} minute{minute(s)}, and {second} second{second(s)}"
            if data["second"] > 0 == data["minute"]:
                fmt += ", and {second} second{second(s)}"
            msg = fmt.format_map(data)
        elif h == 0 and m > 0:
            if data["second"] == 0:
                fmt = "{minute} minute{minute(s)}"
            else:
                fmt = "{minute} minute{minute(s)}, and {second} second{second(s)}"
            msg = fmt.format_map(data)
        elif m == 0 and h == 0 and s > 0:
            fmt = "{second} second{second(s)}"
            msg = fmt.format_map(data)
        elif m == 0 and h == 0 and s == 0:
            msg = "None"
        return msg

    def check_server_settings(self, server):
        if server.id not in self.system["Servers"]:
            self.system["Servers"][server.id] = {"Players": {},
                                                 "Config": {"Steal CD": 5,
                                                            "brownie CD": 5}
                                                 }
            dataIO.save_json(self.file_path, self.system)
            print("Creating default heist settings for Server: {}".format(server.name))
            path = self.system["Servers"][server.id]
            return path
        else:
            path = self.system["Servers"][server.id]
            return path


def check_folders():
    if not os.path.exists("data/brownie"):
        print("Creating data/brownie folder...")
        os.makedirs("data/brownie")


def check_files():
    default = {"Servers": {}}

    f = "data/brownie/brownie.json"
    if not dataIO.is_valid_json(f):
        print("Creating default brownie.json...")
        dataIO.save_json(f, default)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Brownie(bot))
