import discord
from redbot.core import commands

class ChristmasCard(commands.Cog):
  """Send someone a christmas card!"""
  
  def __init__(self, bot):
    self.bot = bot

    @commands.command()
    async def christmascard(self, ctx: commands.Context, user_id: int, *, message: str):
      """Send a christmas card to someone!"""
      destination = self.bot.get_user(user_id)
      if destination is None or destination.bot:
          await ctx.send(
              _(
                  "Invalid ID, user not found, or user is a bot. "
                  "You can only send messages to people I share "
                  "a server with."
              )
          )
          return

        prefixes = await ctx.bot.get_valid_prefixes()
        prefix = re.sub(rf"<@!?{ctx.me.id}>", f"@{ctx.me.name}".replace("\\", r"\\"), prefixes[0])
        description = _("Owner of {}").format(ctx.bot.user)
        content = _("Send christmas cards using {}christmascard!").format(prefix)
        if await ctx.embed_requested():
            e = discord.Embed(colour=discord.Colour.red(), description=message)

            e.set_footer(text=content)
            if ctx.bot.user.avatar_url:
                e.set_author(name=description, icon_url=ctx.bot.user.avatar_url)
            else:
                e.set_author(name=description)

            try:
                await destination.send(embed=e)
            except discord.HTTPException:
                await ctx.send(
                    _("Sorry, I couldn't send a card to {}").format(destination)
                )
            else:
                await ctx.send(_("Message delivered to {}").format(destination))
        else:
            response = "{}\nMessage:\n\n{}".format(description, message)
            try:
                await destination.send("{}\n{}".format(box(response), content))
            except discord.HTTPException:
                await ctx.send(
                    _("Sorry, I couldn't deliver your message to {}").format(destination)
                )
            else:
                await ctx.send(_("Message delivered to {}").format(destination))
