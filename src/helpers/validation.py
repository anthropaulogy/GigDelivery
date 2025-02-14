"""A module containing functions that serve to validate some information."""

import re


def is_valid_location_name(name):
    pattern = r"^[A-Za-z0-9&'., -]+$"
    return bool(re.match(pattern, name))
