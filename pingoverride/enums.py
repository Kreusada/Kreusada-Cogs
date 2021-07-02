from enum import Enum

class PingOverrideVariables(Enum):

    lambda_ = lambda x: (lambda y: getattr(y, x))

    NAME = (
        "The name of the author. This will not include nicknames.",
        lambda_("name")
    )

    ID = (
        "The ID of the author.",
        lambda_("id")
    )

    MENTION = (
        "This variable will allow for the author to be mentioned on response.", 
        lambda_("mention")
    )

    DISCRIMINATOR = (
        "The discriminator of the user.",
        lambda_("discriminator")
    )

    DISPLAY_NAME = (
        "The display name of the author. Will resolve to nickname if the author has one.",
        lambda_("display_name")
    )

    NAME_AND_DISCRIMINATOR = (
        "The name and discriminator of the author (\"user#1234\")",
        lambda x: str(x)
    )

