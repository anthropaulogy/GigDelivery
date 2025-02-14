"""A module that contains generic functions that are not necessarily related."""

import datetime
import uuid


def generate_id() -> uuid.uuid4:
    """Creates a unique ID."""
    return uuid.uuid4()


def get_timestamp() -> datetime.datetime:
    """Creates current timestamp."""
    return datetime.datetime.now()
