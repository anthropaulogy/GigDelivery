import uuid
import pytest

from models.location import Location


@pytest.fixture
def sample_location():
    return Location(
        "Safeway", "Grocery Store", "5100 Broadway", "Oakland", "CA"
    )


@pytest.fixture
def sample_uuid():
    return uuid.uuid4()
