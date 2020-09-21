import discord
from redbot.core import commands
import random
import json
import os


cogs = []

Loaded = False

amounts = {}

name = {}


class Collectable(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _save(self):
        with open('amounts.json', 'w+') as f:
            json.dump(amounts, f)

    @commands.Cog.listener()
    async def on_ready(self):
        global amounts
        try:
            with open('amounts.json') as f:
                amounts = json.load(f)
        except FileNotFoundError:
            print("Could not load amounts.json")
            amounts = {}

    @commands.command("Loaded")
    async def loaded(self, ctx):
        if Loaded == True:
            await ctx.send("Functions loaded")
        else:
            await ctx.send("Functions not loaded!")

    @commands.command("Balance")
    async def balance(self, ctx, user: discord.Member = None):
        if user is not None:
            id = str(user.id)
            if id in amounts.keys():
                currency = amounts[id]
                await ctx.send(f"<@{user.id}> has {currency} in the bank")

            else:
                await ctx.send(f"<@{user.id}> does not have an account!")

        else:
            id = str(ctx.message.author.id)
            if id in amounts.keys():
                await ctx.send("You have {} in the bank!".format(amounts[id]))

            else:
                await ctx.send("You do not have an account!")

    @commands.command("Register")
    async def register(self, ctx, user: discord.Member = None, add=None, subtract=None, currency=None):
        if user is not None:
            if add == "Add" and currency is not None:
                id = str(user.id)
                if id not in amounts.keys():
                    amounts[id] += int(currency)
                    _save()
                else:
                    await ctx.send(f"<@{user.id}> has already been Registered!")
            else:
                if add == "Add" and currency is None:
                    id = str(user.id)
                    if id not in amounts.keys():
                        amounts[id] = 100
                        await ctx.send("No currency was set, defaulting to 100")
                        _save()
                    else:
                        await ctx.send(f"<@{user.id}> has already been Registered!")
                else:
                    if subtract == "Subtract" and currency is not None:
                        id = str(user.id)
                        if id not in amounts.keys():
                            amounts[id] -= int(currency)
                            _save()
                        else:
                            await ctx.send(f"<@{user.id}> has already been Registered!")
                    else:
                        if subtract == "Subtract" and currency is None:
                            id = str(user.id)
                            if id not in amounts.keys():
                                amounts[id] = 100
                                await ctx.send("No currency was set, defaulting to 100")
                                _save()
                            else:
                                await ctx.send(f"<@{user.id}> has already been Registered!")

        else:
            id = str(ctx.message.author.id)
            if id not in amounts.keys():
                amounts[id] = 100
                await ctx.send("You are now registered")
                _save()
            else:
                await ctx.send("You are already registered!")

    @commands.command("Add")
    async def add(self, ctx, currency):
        id = str(ctx.message.author.id)
        if id in amounts.keys():
            balance = amounts[id]
            balance += int(currency)
            amounts[id] = balance
            await ctx.send("Your updated balance is {}".format(amounts[id]))
            _save()

        else:
            await ctx.send("User not registered")

    @commands.command("Subtract")
    async def subtract(self, ctx, currency):
        id = str(ctx.message.author.id)
        if id in amounts.keys():
            balance = amounts[id]
            balance -= int(currency)
            amounts[id] = balance
            await ctx.send("Your updated balance is {}".format(amounts[id]))
            _save()

        else:
            await ctx.send("User not registered")

    @commands.command("Create")
    async def create(self, ctx, user: discord.Member, currency):
        id = str(user.id)
        if id in amounts.keys():
            await ctx.send("User already has an account")
        else:
            amounts[id] += int(currency)
            await ctx.send("Balance is {}".format(amounts[id]))
            _save()

    @commands.command("collectables")
    async def CollectableCreate(self, ctx, action, name, emoji):
        fileName = name + "_system"
        if action == "create" and emoji is not None:
            try:
                file = open(f"{fileName}.json", "x")
                name = {}
                name["emoji"] = emoji
                json.dump(name, file)
                await ctx.send(f"Created ```{fileName}.json``` and collectable")
            except FileExistsError:
                with open(f"{fileName}.json") as f:
                    name = json.load(f)
                    await ctx.send(f"{fileName}.json already exists")

        elif action == "del":
            os.remove(f"{fileName}.json")
            await ctx.send(f"Deleted collecta!ble ```{name}```")

    # @commands.has_role("Moderator")
    @commands.command("collectable")
    async def Collectable(self, ctx, action, name, user: discord.Member, state="add", quantity=0):
        id = str(user.id)
        userNickName = str(user.display_name)
        CollectableID = id + "+" + userNickName
        CollectableName = name
        fileName = name + "_system"
        try:
            with open(f"{fileName}.json") as f:
                name = json.load(f)
        except FileNotFoundError:
            await ctx.send(f"{name} is not a Collectible!")

        if action == "setbalance":
            with open(f"{fileName}.json", "w") as JSONCollectable:
                if CollectableID not in name.keys():
                    name[CollectableID] = 0
                if state == "add":
                    current_balance = name[CollectableID]
                    current_balance += int(quantity)
                    name[CollectableID] = current_balance
                    json.dump(name, JSONCollectable)
                    JSONCollectable.close()
                    await ctx.send(f"<@{user.id}> your updated balance is {name[CollectableID]}")
                elif state == "set":
                    current_balance = name[CollectableID]
                    current_balance = int(quantity)
                    name[CollectableID] = current_balance
                    json.dump(name, JSONCollectable)
                    JSONCollectable.close()
                    await ctx.send(f"<@{user.id}> your updated balance is {name[CollectableID]}")
                elif state == "subtract":
                    current_balance = name[CollectableID]
                    current_balance -= int(quantity)
                    name[CollectableID] = current_balance
                    json.dump(name, JSONCollectable)
                    JSONCollectable.close()
                    await ctx.send(f"<@{user.id}> your updated balance is {name[CollectableID]}")
                else:
                    await ctx.send("Invalid state!")

        elif action == "balance":
            if id not in name.keys():
                await ctx.send(f"That user does not have a {CollectableName} balance!")
            else:
                await ctx.send(f"<@{id}> your {CollectableName} balance is {name[CollectableID]}!")

    @commands.command("cprofile")
    async def Profile(self, ctx, user: discord.Member):
        id = str(user.id)
        userNickName = str(user.display_name)
        CollectableID = id + "+" + userNickName
        HasCollectable = False
        JSON_Collectables = [Collectables for Collectables in os.listdir(
            os.curdir) if Collectables.endswith('.json')]
        embed = discord.Embed(title=f"{user.display_name}'s Collectables!",
                              description=f"{user.display_name}'s Collection")
        for i in range(0, len(JSON_Collectables)):
            with open(f"{JSON_Collectables[i]}") as f:
                data = json.load(f)
                if CollectableID not in data:
                    print("No collectable for user")

                else:
                    HasCollectable = True
                    # print(JSON_Collectables.split('_'))
                    CollectableName = JSON_Collectables[i].split('.')
                    CollectableName = CollectableName[0].split('_')
                    embed.add_field(name=CollectableName[0], value=data[id])
        if HasCollectable is not False:
            await ctx.send(content=None, embed=embed)

        else:
            await ctx.send(f"{user.display_name} has no collectables!")

    @commands.command("leaderboard")
    async def leaders(self, ctx, name):
        FileName = name + "_system"
        with open(f"{FileName}.json") as f:
            values = json.load(f)

        emoji = str(values["emoji"])
        embed = discord.Embed(
            title=f"{name} Leaderboard! {emoji}", description="")
        for key, value in sorted(values.items()):
            if key != "emoji":
                print(value)

        print(sorted(values.items()))

        await ctx.send(content=None, embed=embed)

    @commands.command("Ping")
    async def ping(self, ctx, user: discord.Member):
        await ctx.send("ID is {}".format(user.id))

    @commands.command("Save")
    async def save(self, ctx):
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

        response = random.choice(brooklyn_99_quotes)
        await ctx.send(response)

    @commands.command(name='loadcogs')
    async def LoadCogs(self, ctx, cog_name):
        try:
            bot.load_extension(f"cogs.{cog_name}")
        except commands.ExtensionAlreadyLoaded:
            await ctx.send(f"{cog_name} is loaded.")
        except commands.ExtensionNotFound:
            await ctx.send(f"{cog_name} could not be found")
        else:
            await ctx.send(f"{cog_name} is now Unloaded")
            bot.unload_extension(f"cogs.{cog_name}")
            cogs.append(f"{cog_name}")

    @commands.command(name='cogs')
    async def ListCogs(self, ctx):
        for cog in cogs:
            embed = discord.Embed(title="Cogs", description="Loaded Cogs")
            embed.add_field(name="Cog", value=cog)
            await ctx.send(content=None, embed=embed)
            print(cogs)
