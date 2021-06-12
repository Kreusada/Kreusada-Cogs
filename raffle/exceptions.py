from typing import Literal


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
        return f"({self.key}) The \"{self.key}\" key is required"


class UnknownEntityError(RaffleError):
    """Raised when an invalid role or user is provided to the parser."""

    def __init__(self, data, _type: Literal["user", "role"]):
        self.data = data
        self.type = _type

    def __str__(self):
        return f"\"{self.data}\" was not a valid {self.type}"

class RaffleSyntaxError(RaffleError):
    """Raised when syntax is not provided properly."""
    pass

class RaffleDeprecationWarning(RaffleError):
    """Used for deprecated conditions."""
    pass

class UnidentifiedKeyError(RaffleError):
    """Used when a key is not valid."""
    pass