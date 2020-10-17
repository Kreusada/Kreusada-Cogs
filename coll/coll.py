import discord
from discord.ext import commands
import random
import json
import os


token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

bot = commands.Bot(command_prefix='!')

cogs = []

Loaded = False

amounts = {}

name = {}


@bot.event
async def on_ready():
    global amounts
    try:
        with open('amounts.json') as f:
            amounts = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        amounts = {}
        



def _save():
    with open('amounts.json' , 'w+') as f:
        json.dump(amounts, f)





@bot.command("Loaded")
async def loaded(ctx):
    if Loaded == True:
        await ctx.send("Functions loaded")
    else:
        await ctx.send("Functions not loaded!")

@bot.command("Balance")
async def balance(ctx, user : discord.Member = None):
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

    
    


    
    
   
@bot.command("Register")
async def register(ctx, user: discord.Member=None, add=None, subtract=None, currency=None ):
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
            

@bot.command("Add")
async def add(ctx, currency):
    id = str(ctx.message.author.id)
    if id in amounts.keys():
        balance = amounts[id]
        balance += int(currency)
        amounts[id] = balance
        await ctx.send("Your updated balance is {}".format(amounts[id]))
        _save()

    else:
        await ctx.send("User not registered")

@bot.command("Subtract")
async def subtract(ctx, currency):
    id = str(ctx.message.author.id)
    if id in amounts.keys():
        balance = amounts[id]
        balance -= int(currency)
        amounts[id] = balance
        await ctx.send("Your updated balance is {}".format(amounts[id]))
        _save()

    else:
        await ctx.send("User not registered")

@bot.command("Create")
async def create(ctx, user: discord.Member, currency):
    id = str(user.id)
    if id in amounts.keys():
        await ctx.send("User already has an account")
    else:
        amounts[id] += int(currency)
        await ctx.send("Balance is {}".format(amounts[id]))
        _save()


@bot.command("collectables")
async def CollectableCreate(ctx, action, name, emoji):
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

#@commands.has_role("Moderator")
@bot.command("collectable")
async def Collectable(ctx, action, name, user: discord.Member, state="add", quantity=0):
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
        
        

  

    


@commands.has_role("Moderators")
@bot.command("cprofile")
async def Profile(ctx, user: discord.Member):
    id = str(user.id)
    userNickName = str(user.display_name)
    CollectableID = id + "+" + userNickName
    HasCollectable = False
    JSON_Collectables = [Collectables for Collectables in os.listdir(os.curdir) if Collectables.endswith('.json')]
    embed = discord.Embed(title=f"{user.display_name}'s Collectables!", description = f"{user.display_name}'s Collection")
    for i in range(0, len(JSON_Collectables)):
        with open(f"{JSON_Collectables[i]}") as f:
            data = json.load(f)
            if CollectableID not in data:
                print("No collectable for user")
                
            else:
                HasCollectable = True
                #print(JSON_Collectables.split('_'))
                CollectableName = JSON_Collectables[i].split('.')
                CollectableName = CollectableName[0].split('_')
                embed.add_field(name=CollectableName[0], value=data[id])
    if HasCollectable is not False:
        await ctx.send(content=None, embed=embed)
        
    else:
        await ctx.send(f"{user.display_name} has no collectables!")
    
    
    

@bot.command("leaderboard")
async def LeaderBoard(ctx, name):
    FileName = name + "_system"
    with open(f"{FileName}.json") as f:
        values = json.load(f)
    
    
    emoji = str(values["emoji"])
    embed = discord.Embed(title=f"{name} Leaderboard! {emoji}", description = "")
    for key, value in sorted(values.items()):
        if key != "emoji":
            print(value)
            
            

    print(sorted(values.items()))
            

    await ctx.send(content=None, embed=embed)
        
        


    





@bot.command("Ping")
async def Ping(ctx, user : discord.Member):
    await ctx.send("ID is {}".format(user.id))
  
@bot.command("Save")
async def save(ctx):
    _save()

    
   


@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
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

@bot.command(name='loadcogs')
async def LoadCogs(ctx, cog_name):
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
        

        
        



@bot.command(name='cogs')
async def ListCogs(ctx):
    for cog in cogs:
        embed = discord.Embed(title="Cogs", description = "Loaded Cogs")
        embed.add_field(name="Cog", value=cog)
        await ctx.send(content=None, embed=embed)
        print(cogs)

    


bot.run(token)

