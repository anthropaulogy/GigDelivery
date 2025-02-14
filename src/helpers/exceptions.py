"""A module containing custom exceptions"""


class InvalidIDError(Exception):
    def __init__(self, message: str = "Invalid ID") -> None:
        super().__init__(message)


class InvalidLocationName(Exception):
    def __init__(self, message: str = "Invalid location name") -> None:
        super().__init__(message)
