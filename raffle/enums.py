import enum

class RaffleComponents(enum.Enum):
    """All of the components which can be
    used in a raffle. This class is mainly
    used for the ``[p]raffle conditions`` command.
    """

    name = (
        str, 
        "The name of the raffle. This is the only REQUIRED field."
    )

    description = (
        str, 
        "The description for the raffle. This information appears in the raffle info command."
    )

    end_message = (
        str,
        "The message used to end the raffle. Defaults to \"Congratulations {winner.mention}, you have won the {raffle} raffle!\""
    )

    account_age = (
        int, 
        "The account age requirement for the user who joins the raffle. This must be specified in days."
    )

    join_age = (
        int, 
        "The number of days the user needs to be in the server for in order to join the raffle."
    )

    roles_needed_to_enter = (
        list, 
        "A list of discord roles which the user must have in order to join the raffle. These MUST be specified using IDs."
    )

    prevented_users = (
        list, 
        "A list of discord users who are not allowed to join the raffle. These MUST be specified using IDs."
    )

    allowed_users = (
        list,
        "A list of discord users who are allowed to join the raffle. If this condition exists, no one will be able to join apart from those in the list."
    )

    maximum_entries = (
        int, 
        "The maximum number of entries allowed for a raffle."
    )

    on_end_action = (
        str,
        "The action to perform when a user is drawn. Must be one of 'end', 'remove_winner', or 'keep_winner', defaults to 'keep_winner'."
    )
