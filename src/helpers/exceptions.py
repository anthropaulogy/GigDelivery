"""A module containing custom exceptions"""


class IDExistsError(Exception):
    def __init__(self, message: str = "ID is not unique") -> None:
        super().__init__(message)


class IDNotFoundError(Exception):
    def __init__(self, message: str = "ID was not found") -> None:
        super().__init__(message)


class InvalidIDError(Exception):
    def __init__(self, message: str = "Invalid ID") -> None:
        super().__init__(message)


class InvalidLocationNameError(Exception):
    def __init__(self, message: str = "Invalid location name") -> None:
        super().__init__(message)


class InvalidLocationTypeError(Exception):
    def __init__(self, message: str = "Invalid location type") -> None:
        super().__init__(message)
