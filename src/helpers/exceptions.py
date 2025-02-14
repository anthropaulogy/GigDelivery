"""A module containing custom exceptions"""


class InvalidIDError(Exception):
    """A exception for an invalid ID"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message
