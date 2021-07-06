import enum
from typing import Any, Dict, List, Type, Union

from redbot.core.i18n import Translator

from .exceptions import (
    InvalidArgument,
    RaffleError,
    RaffleSyntaxError,
    RequiredKeyError,
    UnknownEntityError,
)

_ = Translator("Raffle", __file__)
ComponentsDictionary = Dict[str, Union[str, bool, List[Type[Union[Any, RaffleError]]]]]

__all__ = (
    "RaffleEndMessageComponents",
    "RaffleJoinMessageComponents",
    "RaffleComponents",
)


class RaffleEndMessageComponents(enum.Enum):
    """A list of variables and attributes
    available for the raffle end_message block."""

    raffle = _("The name of the raffle when the end_message is used.")

    winner__name = _("The username of the winner.")
    winner__mention = _("The mention of the winner.")
    winner__id = _("The ID of the winner.")
    winner__display_name = _("The display name of the winner.")
    winner__discriminator = _("The discriminator of the winner.")
    winner__name_and_discriminator = _("The name and discriminator of the winner (user#1234).")


class RaffleJoinMessageComponents(enum.Enum):
    """A list of variables and attributes
    available for the raffle join_message block."""

    raffle = _("The name of the raffle when the end_message is used.")
    entry_count = _("The number of entries in the raffle.")

    user__name = _("The username of the user.")
    user__mention = _("The mention of the user.")
    user__id = _("The ID of the user.")
    user__display_name = _("The display name of the user.")
    user__discriminator = _("The discriminator of the user.")
    user__name_and_discriminator = _("The name and discriminator of the user (user#1234).")


class ComponentDescriptions(enum.Enum):
    NAME = _(
        "The name for the raffle. This name is not changeable once the "
        "raffle has been created. If you wish to rename the raffle, use "
        "the `[p]raffle asyaml` command, and copy across the settings "
        "with a different name."
    )
    DESCRIPTION = _(
        "The description for the raffle. This text will appear in various "
        "informative commands such as `[p]raffle list`, and `[p]raffle info`. "
        "You can use this condition to give your users an explanation of what "
        "the raffle is about, how the winners can claim their prize..."
    )
    JOIN_MESSAGE = _(
        "This condition allows you to customise a section of the message "
        "that is sent when a user joins a raffle. You can use various "
        "variables in this message too."
    )
    END_MESSAGE = _(
        "This condition allows you to customise a section of the message "
        "that is sent when a user is drawn from a raffle. You can use various "
        "variables in this message too."
    )
    ACCOUNT_AGE = _(
        "This condition allows you to block users from joining the raffle "
        "if their account age in DAYS is fewer than the provided condition."
    )
    SERVER_JOIN_AGE = _(
        "This condition allows you to block users from joining the raffle "
        "if they have been in the server for less DAYS than the provided condition."
    )
    ROLES_NEEDED_TO_ENTER = _(
        "A list of Discord role IDs which the user must have in order to "
        "join the raffle. They must be provided as IDs in a list."
    )
    BADGES_NEEDED_TO_ENTER = _(
        "A list of Discord badges which the user must have in order to "
        "join the raffle. They must be provided as badge names in a list."
    )
    PREVENTED_USERS = _(
        "A list of Discord user IDs, of users who who will not be able to "
        "join the raffle. They must be provided as IDs in a list."
    )
    ALLOWED_USERS = _(
        "A list of Discord user IDs, of users who who will be able to "
        "join the raffle. They must be provided as IDs in a list. If "
        "this condition is not provided normally, anyone will be allowed "
        "in the raffle. It's useful for when you only want particular users "
        "to be able to join a raffle."
    )
    MAXIMUM_ENTRIES = _(
        "This condition allows you to only allow a certain amount of server "
        "entries into a raffle. Once this limit has been reached, no more users "
        "will be able to join the raffle."
    )
    ON_END_ACTION = _(
        "This condition allows you to decide what happens when a user is drawn from "
        "a raffle. This must be one of 'end', 'keep_winner', 'remove_winner', or "
        "'remove_and_prevent_winner'."
    )


class ComponentExamples(enum.Enum):
    NAME = "my_raffle"
    DESCRIPTION = "My very first raffle!"
    JOIN_MESSAGE = (
        r"Welcome to the {raffle} raffle {user.mention}! There are now {entry_count} entries."
    )
    END_MESSAGE = r"Congrats {winner.mention} - you just won the **{raffle}** raffle! :tada:"
    ACCOUNT_AGE = 50
    SERVER_JOIN_AGE = 30
    ROLES_NEEDED_TO_ENTER = [749272596050214973, 778743725790068766]
    BADGES_NEEDED_TO_ENTER = ["verified_bot_developer", "bug_hunter"]
    PREVENTED_USERS = [719988449867989142]
    ALLOWED_USERS = [719988449867989142]
    MAXIMUM_ENTRIES = 10
    ON_END_ACTION = "remove_and_prevent_winner"


class RaffleComponents(enum.Enum):
    """All of the components which can be
    used in a raffle. This class is mainly
    used for the ``[p]raffle conditions`` command.
    """

    name: ComponentsDictionary = {
        "supported_types": [str],
        "potential_exceptions": [RaffleSyntaxError, RequiredKeyError],
        "variables": None,
        "required_condition": True,
        "description": ComponentDescriptions.NAME.value,
        "example": ComponentExamples.NAME.value,
    }

    description: ComponentsDictionary = {
        "supported_types": [str],
        "potential_exceptions": [RaffleSyntaxError],
        "variables": None,
        "required_condition": False,
        "description": ComponentDescriptions.DESCRIPTION.value,
        "example": ComponentExamples.DESCRIPTION.value,
    }

    join_message: ComponentsDictionary = {
        "supported_types": [str],
        "potential_exceptions": [RaffleSyntaxError, InvalidArgument],
        "variables": [x.name for x in RaffleJoinMessageComponents],
        "required_condition": False,
        "description": ComponentDescriptions.JOIN_MESSAGE.value,
        "example": ComponentExamples.JOIN_MESSAGE.value,
    }

    end_message: ComponentsDictionary = {
        "supported_types": [str],
        "potential_exceptions": [RaffleSyntaxError, InvalidArgument],
        "variables": [x.name for x in RaffleEndMessageComponents],
        "required_condition": False,
        "description": ComponentDescriptions.END_MESSAGE.value,
        "example": ComponentExamples.END_MESSAGE.value,
    }

    account_age: ComponentsDictionary = {
        "supported_types": [int],
        "potential_exceptions": [RaffleSyntaxError],
        "variables": None,
        "required_condition": False,
        "description": ComponentDescriptions.ACCOUNT_AGE.value,
        "example": ComponentExamples.ACCOUNT_AGE.value,
    }

    server_join_age: ComponentsDictionary = {
        "supported_types": [int],
        "potential_exceptions": [RaffleSyntaxError],
        "variables": None,
        "required_condition": False,
        "description": ComponentDescriptions.SERVER_JOIN_AGE.value,
        "example": ComponentExamples.SERVER_JOIN_AGE.value,
    }

    roles_needed_to_enter: ComponentsDictionary = {
        "supported_types": [list],
        "potential_exceptions": [RaffleSyntaxError, UnknownEntityError],
        "variables": None,
        "required_condition": False,
        "description": ComponentDescriptions.ROLES_NEEDED_TO_ENTER.value,
        "example": ComponentExamples.ROLES_NEEDED_TO_ENTER.value,
    }

    badges_needed_to_enter: ComponentsDictionary = {
        "supported_types": [list],
        "potential_exceptions": [RaffleSyntaxError, InvalidArgument],
        "variables": None,
        "required_condition": False,
        "description": ComponentDescriptions.BADGES_NEEDED_TO_ENTER.value,
        "example": ComponentExamples.BADGES_NEEDED_TO_ENTER.value,
    }

    prevented_users: ComponentsDictionary = {
        "supported_types": [list],
        "potential_exceptions": [RaffleSyntaxError, UnknownEntityError],
        "variables": None,
        "required_condition": False,
        "description": ComponentDescriptions.PREVENTED_USERS.value,
        "example": ComponentExamples.PREVENTED_USERS.value,
    }

    allowed_users: ComponentsDictionary = {
        "supported_types": [list],
        "potential_exceptions": [RaffleSyntaxError, UnknownEntityError],
        "variables": None,
        "required_condition": False,
        "description": ComponentDescriptions.ALLOWED_USERS.value,
        "example": ComponentExamples.ALLOWED_USERS.value,
    }

    maximum_entries: ComponentsDictionary = {
        "supported_types": [int],
        "potential_exceptions": [RaffleSyntaxError],
        "variables": None,
        "required_condition": False,
        "description": ComponentDescriptions.MAXIMUM_ENTRIES.value,
        "example": ComponentExamples.MAXIMUM_ENTRIES.value,
    }

    on_end_action: ComponentsDictionary = {
        "supported_types": [str],
        "potential_exceptions": [InvalidArgument],
        "variables": None,
        "required_condition": False,
        "description": ComponentDescriptions.ON_END_ACTION.value,
        "example": ComponentExamples.ON_END_ACTION.value,
    }
