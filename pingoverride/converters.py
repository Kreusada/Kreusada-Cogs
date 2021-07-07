from redbot.core.commands import BadArgument, Context, Converter


class EmbedTitle(Converter):
    async def convert(self, ctx: Context, argument: str):
        if len(argument) > 256:
            raise BadArgument("Your title must be 256 characters or fewer.")
        return argument
