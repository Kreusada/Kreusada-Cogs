from redbot.core import commands
import random
import json
import os
import discord
from discord.utils import get
from copy import copy


amounts = {}


def _save():
    """Saves the amounts to a json
    """
    with open('testing.json', 'w+') as f:
        json.dump(amounts, f)


class Collectables(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            with open('testing.json') as f:
                amounts = json.load(f)
        except FileNotFoundError:
            owner_id = self.bot.get_user(544974305445019651)
            await owner_id.send("File not found.")
            amounts = {}

    @commands.command()
    async def balance(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        if str(user.id) in amounts.keys():
            await ctx.send("{0.display_name} has {1} in the bank".format(user, amounts[str(user.id)]))
        else:
            await ctx.send("{0.display_name} does not have an account".format(user))

    @commands.command()
    async def register(self, ctx):
        if str(ctx.author.id) not in amounts.keys():
            amounts[str(ctx.author.id)] = 100
            _save()
            await ctx.send("You have now been registered!")
        else:
            await ctx.send("You have already been registered!")

    # @register.command(name="add")
    # async def _add(self, ctx, user: commands.Greedy[discord.Member] = None, currency: int = 100):
    #     if user is None:
    #         user = ctx.author

    #     if str(user.id) not in amounts.keys():
    #         amounts[str(user.id)] = currency
    #         await ctx.send("{0.mention} has been registered!".format(user))
    #     else:
    #         await ctx.send("{0.mention} has already been registered!\nPlease use the `add` command to change their bank values".format(user))

    # @register.command(name="subtract", aliases=["sub"])
    # async def _subtract(self, ctx, user: commands.Greedy[discord.Member] = None, currency: int = 100):
    #     if user is None:
    #         user = ctx.author
    #     if str(user.id) not in amounts.keys():
    #         amounts[str(user.id)] = currency
    #         await ctx.send("{0.mention} has been registered!".format(user))
    #     else:
    #         await ctx.send("{0.mention} has already been registered!\nPlease use the `subtract` command to change their bank values".format(user))

    @commands.command()
    async def subtract(self, ctx, currency: int = 100):
        if str(ctx.author.id) in amounts.keys():
            # balance = amounts[str(ctx.author.id)]
            # balance -= int(currency)
            # amounts[str(ctx.author.id)] = balance
            amounts[str(ctx.author.id)] -= currency
            await ctx.send("Your updated balance is {0}".format(amounts[str(ctx.author.id)]))
            _save()

        else:
            await ctx.send("{0.mention} not registered!\nPlease use the register command!".format(ctx.author))

    @commands.command(name="add")
    async def add(self, ctx, currency: int = None):
        if currency is None:
            currency = 10
        if str(ctx.author.id) in amounts.keys():
            amounts[str(ctx.author.id)] += currency
            _save()
            await ctx.send("Your updated balance is {0}".format(amounts[str(ctx.author.id)]))
        else:
            await ctx.send("You haven't been registered yet!")

    @commands.command()
    async def collectablecreate(self, ctx, action, name, emoji):
        file_name = name + "_system"
        if action == "create" and emoji is not None:
            try:
                file = open(f"{file_name}.json", "x")
                name = {}
                name["emoji"] = emoji
                json.dump(name, file)
                await ctx.send(f"Created ```{file_name}.json``` and collectable")
            except FileExistsError:
                with open(f"{file_name}.json") as f:
                    name = json.load(f)
                    await ctx.send(f"{file_name}.json already exists")

        elif action == "del":
            os.remove(f"{file_name}.json")
            await ctx.send(f"Deleted collecta!ble ```{name}```")

    @commands.group()
    async def collectable(self, ctx):
        pass
        # id = str(user.id)
        # user_nick = str(user.display_name)
        # collectable_id = id + "+" + user_nick
        # collectable_name = name
        # file_name = name + "_system"
        # try:
        #     with open(f"{file_name}.json") as f:
        #         name = json.load(f)
        # except FileNotFoundError:
        #     await ctx.send(f"{name} is not a Collectible!")

        # if action == "setbalance":
        #     with open(f"{file_name}.json", "w") as JSONCollectable:
        #         if collectable_id not in name.keys():
        #             name[collectable_id] = 0

        #         if state == "add":
        #             current_balance = name[collectable_id]
        #             current_balance += int(quantity)
        #             name[collectable_id] = current_balance
        #             json.dump(name, JSONCollectable)
        #             JSONCollectable.close()
        #             await ctx.send(f"<@{user.id}> your updated balance is {name[collectable_id]}")

        #         elif state == "set":
        #             current_balance = name[collectable_id]
        #             current_balance = int(quantity)
        #             name[collectable_id] = current_balance
        #             json.dump(name, JSONCollectable)
        #             JSONCollectable.close()
        #             await ctx.send(f"<@{user.id}> your updated balance is {name[collectable_id]}")

        #         elif state == "subtract":
        #             current_balance = name[collectable_id]
        #             current_balance -= int(quantity)
        #             name[collectable_id] = current_balance
        #             json.dump(name, JSONCollectable)
        #             JSONCollectable.close()
        #             await ctx.send(f"<@{user.id}> your updated balance is {name[collectable_id]}")
        #         else:
        #             await ctx.send("Invalid state!")

        # elif action == "balance":
        #     if id not in name.keys():
        #         await ctx.send(f"That user does not have a {collectable_name} balance!")
        #     else:
        #         await ctx.send(f"<@{id}> your {collectable_name} balance is {name[collectable_id]}!")

    @collectable.group(name="setbal", aliases=["sb", "setb"])
    async def set_balance(self, ctx):  # , user):
        pass

    @set_balance.command(name="add")
    async def collectable_add(self, ctx, name, currency: int = 100):
        collectable_id = "{0}+{1}".format(str(ctx.author.id),
                                          str(ctx.author.display_name))
        file_name = "{0}_system".format(name)
        try:
            with open("{0}.json".format(file_name), "r") as f:
                name = json.load(f)
        except FileNotFoundError:
            await ctx.send("{0} is not a collectable!".format(name))
        with open("{0}.json", "w") as COLLECTABLEJSON:
            if collectable_id not in name.keys():
                name[collectable_id] = 0

            name[collectable_id] += currency
            json.dump(name, COLLECTABLEJSON, indent=4)
            await ctx.send("{0.display_name} you have {1}".format(ctx.author, name[collectable_id]))

    @commands.command()
    async def cprofile(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        id = str(user.id)
        user_nick = str(user.display_name)
        collectable_id = id + "+" + user_nick
        has_collectable = False
        json_collectables = [Collectables for Collectables in os.listdir(
            os.curdir) if Collectables.endswith('.json')]
        embed = discord.Embed(title=f"{user.display_name}'s Collectables!",
                              description=f"{user.display_name}'s Collection")
        for i in range(0, len(json_collectables)):
            with open(f"{json_collectables[i]}") as f:
                data = json.load(f)
                if collectable_id not in data:
                    print("No collectable for user")

                else:
                    has_collectable = True
                    # print(json_collectables.split('_'))
                    collectable_name = json_collectables[i].split('.')
                    collectable_name = collectable_name[0].split('_')
                    embed.add_field(name=collectable_name[0], value=data[id])
        if has_collectable is not False:
            await ctx.send(content=None, embed=embed)

        else:
            await ctx.send(f"{user.display_name} has no collectables!")

    @commands.command()
    async def cleaderboard(self, ctx, name):
        file_name = name + "_system"
        with open(f"{file_name}.json") as f:
            values = json.load(f)

        emoji = str(values["emoji"])
        embed = discord.Embed(
            title=f"{name} Leaderboard! {emoji}", description="")
        for key, value in sorted(values.items()):
            if key != "emoji":
                print(value)

        print(sorted(values.items()))

        await ctx.send(content=None, embed=embed)

    @commands.command()
    @commands.is_owner()
    async def save(self, ctx):
        """Runs the _save() function
        """
        _save()
        await ctx.send("Saved")

    @commands.command(name='99', help='Responds with a random quote from Brooklyn 99')
    async def nine_nine(self, ctx):
        brooklyn_99_quotes = [
            'I\'m the human form of the 💯 emoji.',
            'Bingpot!',
            (
                'Cool. Cool cool cool cool cool cool cool, '
                'no doubt no doubt no doubt no doubt.'
            ),
        ]

        # response = random.choice(brooklyn_99_quotes)
        await ctx.send(random.choice(brooklyn_99_quotes))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sudo(self, ctx, user: discord.Member, *, command):
        """Sudo another user invoking a command.
        The prefix must not be entered.
        """
        msg = copy(ctx.message)
        msg.author = user
        msg.content = ctx.prefix + command

        ctx.bot.dispatch("message", msg)

    @commands.command(hidden=True, name="amounts")
    @commands.is_owner()
    async def ramounts(self, ctx):
        x = "".join(amounts)
        await ctx.send(x)
