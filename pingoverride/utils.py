import asyncio

from redbot.core import commands
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.predicates import MessagePredicate

from .objects import Member


def curl(t):
    return "{{{}}}".format(t)


async def add_random_messages(ctx, original_ping_message):
    await ctx.send("Would you like to add more messages to select from at random? (y/n)")
    try:
        pred = MessagePredicate.yes_or_no(ctx, user=ctx.author)
        await ctx.bot.wait_for("message", check=pred, timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond, I assumed yes.")
        return original_ping_message
    if pred.result:
        await ctx.send(
            "Keep adding messages until you are satisfied. Type **stop()** to stop gathering messages."
        )
        check = lambda x: x.author == ctx.author and x.channel == ctx.channel
        messages = [original_ping_message]
        while True:
            await ctx.send("Add a random response:")
            try:
                message = await ctx.bot.wait_for("message", check=check, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send(
                    f"You took too long to respond - gathered {len(messages)} messages."
                )
                return messages
            if message.content.lower() in ("stop()", "exit()", "quit()"):
                await ctx.send(f"Stopping - gathered {len(messages)} messages.")
                return messages
            try:
                message.content.format(
                    author=Member(ctx.author), latency=round(ctx.bot.latency * 1000, 2)
                )
            except KeyError as e:
                curled = curl(str(e).strip("'"))
                await ctx.send(f"{curled} is not a recognized variable, skipping...")
                continue
            except commands.BadArgument as e:
                curled = curl(f"author.{e}")
                await ctx.send(f"{curled} is not valid, author has no attribute {e}, skipping...")
                continue
            messages.append(message.content)
    else:
        return original_ping_message
