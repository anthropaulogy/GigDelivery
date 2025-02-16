"""A module containing functions that serve to validate some information."""

import re

from helpers import reference


def is_valid_location_name(name) -> bool:
    pattern = r"^[A-Za-z0-9&'., -]+$"
    return bool(re.match(pattern, name))


def is_valid_location_type(location_type: str) -> bool:
    return location_type in reference.location_types
