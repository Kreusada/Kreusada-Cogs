from typing import Literal

from redbot.core.i18n import Translator

_ = Translator("Raffle", __file__)

__all__ = (
    "RaffleError",
    "RequiredKeyError",
    "UnknownEntityError",
    "RaffleSyntaxError",
    "RaffleDeprecationWarning",
    "UnidentifiedKeyError",
    "InvalidArgument",
)


class RaffleError(Exception):
    """Base exception for all raffle exceptions.

    These exceptions are raised, but then formatted
    in an except block to create a user-friendly
    error in which the user can read and improve from."""

    pass


class RequiredKeyError(RaffleError):
    """Raised when a raffle key is required."""

    def __init__(self, key):
        self.key = key

    def __str__(self):
        return _('({0.key}) The "{0.key}" key is required'.format(self))


class UnknownEntityError(RaffleError):
    """Raised when an invalid role or user is provided to the parser."""

    def __init__(self, data, _type: Literal["user", "role"]):
        self.data = data
        self.type = _type

    def __str__(self):
        return _('"{0.data}" was not a valid {0.type}'.format(self))


class RaffleSyntaxError(RaffleError):
    """Raised when syntax is not provided properly."""

    pass


class RaffleDeprecationWarning(RaffleError):
    """Used for deprecated conditions."""

    pass


class UnidentifiedKeyError(RaffleError):
    """Used when a key is not valid."""

    pass


class InvalidArgument(RaffleError):
    """Used when an invalid argument is provided."""

    pass
