import enum

class RaffleEMC(enum.Enum):
    """A list of variables and attributes
    available for the raffle end_message block."""

    raffle = "The name of the raffle when the end_message is used."

    winner__name = "The username of the winner."
    winner__mention = "The mention of the winner."
    winner__id = "The ID of the winner."
    winner__display_name = "The display name of the winner."
    winner__discriminator = "The discriminator of the winner."
    winner__name_and_discriminator = "The name and discriminator of the winner (user#1234)."


class RaffleJMC(enum.Enum):
    """A list of variables and attributes
    available for the raffle join_message block."""

    raffle = "The name of the raffle when the end_message is used."
    entry_count = "The number of entries in the raffle."

    user__name = "The username of the user."
    user__mention = "The mention of the user."
    user__id = "The ID of the user."
    user__display_name = "The display name of the user."
    user__discriminator = "The discriminator of the user."
    user__name_and_discriminator = "The name and discriminator of the user (user#1234)."


class RaffleComponents(enum.Enum):
    """All of the components which can be
    used in a raffle. This class is mainly
    used for the ``[p]raffle conditions`` command.
    """

    name = (
        "The name of the raffle. This is the only REQUIRED field."
    )

    description = (
        "The description for the raffle. This information appears in the raffle info command."
    )

    join_message = (
        "The message sent when a user joins the raffle."
    )

    end_message = (
        "The message used to end the raffle. Defaults to \"Congratulations {winner.mention}, you have won the {raffle} raffle!\""
    )

    account_age = (
        "The account age requirement for the user who joins the raffle. This must be specified in days."
    )

    join_age = (
        "The number of days the user needs to be in the server for in order to join the raffle."
    )

    roles_needed_to_enter = (
        "A list of discord roles which the user must have in order to join the raffle. These MUST be specified using IDs."
    )

    prevented_users = (
        "A list of discord users who are not allowed to join the raffle. These MUST be specified using IDs."
    )

    allowed_users = (
        "A list of discord users who are allowed to join the raffle. If this condition exists, no one will be able to join apart from those in the list."
    )

    maximum_entries = (
        "The maximum number of entries allowed for a raffle."
    )

    on_end_action = (
        "The action to perform when a user is drawn. Must be one of 'end', 'remove_winner', or 'keep_winner', defaults to 'keep_winner'."
    )
