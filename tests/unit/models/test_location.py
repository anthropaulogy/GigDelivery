import pytest
import uuid
import datetime
from models.location import Location  # type: ignore
from helpers import exceptions


def test_location_instance(sample_location):
    assert isinstance(sample_location, Location)
    assert isinstance(sample_location.location_id, uuid.UUID)
    assert sample_location.location_name == "Safeway"
    assert sample_location.location_type == "Grocery Store"
    assert sample_location.street_address == "5100 Broadway"
    assert sample_location.city == "Oakland"
    assert sample_location.state == "CA"
    assert isinstance(sample_location.location_created, datetime.datetime)


def test_add_delivery_to_location_with_valid_uuid(
    sample_location, sample_uuid
):
    assert len(sample_location.deliveries_at_location) == 0

    sample_location.add_delivery_to_location(sample_uuid)

    assert len(sample_location.deliveries_at_location) == 1
    assert isinstance(sample_location.deliveries_at_location[0], uuid.UUID)
    assert sample_location.deliveries_at_location[0] == sample_uuid


def test_add_delivery_to_location_with_different_ids(
    sample_location, sample_uuid
):
    sample_location.add_delivery_to_location(sample_uuid)
    assert sample_location.deliveries_at_location[0] != uuid.uuid4()


def test_add_delivery_to_location_with_invalid_uuid(sample_location):
    with pytest.raises(exceptions.InvalidIDError):
        sample_location.add_delivery_to_location("NotID")


def test_add_delivery_to_location_with_existing_id(
    sample_location, sample_uuid
):
    # Add ID
    sample_location.add_delivery_to_location(sample_uuid)

    # Add ID again
    with pytest.raises(exceptions.IDExistsError):
        sample_location.add_delivery_to_location(sample_uuid)


def test_increase_and_decrease_delivery_count(sample_location):
    # Increase the count
    sample_location.increase_delivery_count()
    assert sample_location.delivery_count == 1

    # Decrease the count
    sample_location.decrease_delivery_count()
    assert sample_location.delivery_count == 0


def test_format_label(sample_location):
    assert sample_location.format_label() == "Safeway (5100 Broadway)"


def test_remove_delivery_from_location_with_valid_id(
    sample_location, sample_uuid
):
    # Add delivery ID to location
    sample_location.add_delivery_to_location(sample_uuid)

    # Remove ID from location
    sample_location.remove_delivery_from_location(sample_uuid)
    assert len(sample_location.deliveries_at_location) == 0


def test_remove_delivery_from_location_with_invalid_id(sample_location):
    with pytest.raises(exceptions.InvalidIDError):
        sample_location.remove_delivery_from_location("NotID")


def test_remove_delivery_from_location_with_id_not_found(
    sample_location, sample_uuid
):
    with pytest.raises(exceptions.IDNotFoundError):
        sample_location.remove_delivery_from_location(sample_uuid)


def test_location_name_setter_with_valid_name(sample_location):
    sample_location.location_name = "Successful Name"
    assert sample_location.location_name == "Successful Name"


def test_location_name_setter_with_invalid_name(sample_location):
    with pytest.raises(exceptions.InvalidLocationNameError):
        sample_location.location_name = "#@%"


def test_location_type_setter_with_valid_location_type(sample_location):
    sample_location.location_type = "Customer"
    assert sample_location.location_type == "Customer"


def test_location_type_setter_with_invalid_location_type(sample_location):
    with pytest.raises(exceptions.InvalidLocationTypeError):
        sample_location.location_type = "asdfasdf"


def test_comparing_locations(sample_location):
    sample_location_2 = Location(
        "Test Location", "Customer", "555 Fake Street", "Faketown", "CA"
    )

    assert sample_location != sample_location_2


def test_location_repr(sample_location):
    print([sample_location])


def test_printing_location(sample_location):
    print(sample_location)
