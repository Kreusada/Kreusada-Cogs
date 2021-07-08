from enum import Enum


class PingOverrideVariables(Enum):

    lambda_ = lambda x: lambda y: getattr(y, x)

    NAME = (
        lambda_("name"),
        "The name of the author. This will not include nicknames.",
        "Wumpus",
    )

    ID = (lambda_("id"), "The ID of the author.", "1234567890122345678")

    MENTION = (
        lambda_("mention"),
        "This variable will allow for the author to be mentioned on response.",
        "<@!1234567890122345678>",
    )

    DISCRIMINATOR = (lambda_("discriminator"), "The discriminator of the user.", "0001")

    DISPLAY_NAME = (
        lambda_("display_name"),
        "The display name of the author. Will resolve to nickname if the author has one.",
        "Wumpus nickname 123",
    )

    NAME_AND_DISCRIMINATOR = (
        lambda x: str(x),
        "The name and discriminator of the author (user#1234)",
        "Wumpus#0001",
    )

    LATENCY = (None, "The bot's latency rounded to 2 decimal places.", "104.54")
