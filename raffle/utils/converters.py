from redbot.core.commands import BadArgument, Context, Converter

__all__ = (
    "RaffleFactoryConverter",
    "RaffleExists",
)


class RaffleFactoryConverter(Converter):
    """A checker which raises BadArgument if the
    author is not the owner of a raffle or the owner
    of the guild, or if the raffle doesn't exist."""

    async def convert(self, ctx: Context, argument: str):
        async with ctx.cog.config.guild(ctx.guild).raffles() as raffles:
            if not argument in raffles.keys():
                raise BadArgument(
                    "There is not an ongoing raffle with the name `{}`.".format(argument)
                )
            if ctx.author.id not in (raffles[argument]["owner"], ctx.guild.owner_id):
                raise BadArgument("You are not the owner of this raffle.")
        return argument


class RaffleExists(Converter):
    """A checker which raises BadArgument
    if the raffle doesn't exist."""

    async def convert(self, ctx: Context, argument: str):
        async with ctx.cog.config.guild(ctx.guild).raffles() as raffles:
            if not argument in raffles.keys():
                raise BadArgument(
                    "There is not an ongoing raffle with the name `{}`.".format(argument)
                )
        return argument
