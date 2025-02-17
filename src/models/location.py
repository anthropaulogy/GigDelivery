import datetime
import uuid
from helpers import utils, validation, exceptions


class Location:
    """Represents a location on a delivery.

    Serves as a unique address.  Multiple copies of same location should not exist.
    """

    def __init__(
        self,
        location_name: str,
        location_type: str,
        street_address: str,
        city: str,
        state: str,
    ) -> None:
        self.__location_id: uuid.UUID = utils.generate_id()
        self.__location_name: str = location_name
        self.__location_type: str = location_type
        self.__street_address: str = street_address
        self.__city: str = city
        self.__state: str = state
        self.__deliveries_at_location: list[uuid.UUID] = []
        self.__delivery_count: int = 0
        self.__location_created: datetime.datetime = utils.get_timestamp()

    # [ METHODS ] -------------------------------------------------------------

    def add_delivery_to_location(self, delivery_id: uuid.UUID) -> None:
        """Adds a delivery ID to Location when delivery is made and increases the count."""
        if not isinstance(delivery_id, uuid.UUID):
            raise exceptions.InvalidIDError()

        if delivery_id in self.deliveries_at_location:
            raise exceptions.IDExistsError()

        self.__deliveries_at_location.append(delivery_id)
        self.increase_delivery_count()

    def decrease_delivery_count(self) -> None:
        """Decrease the delivery count."""
        if self.__delivery_count > 0:
            self.__delivery_count -= 1

    def format_label(self) -> str:
        """Provides a generic label for location name and address."""
        return f"{self.__location_name} ({self.__street_address})"

    def increase_delivery_count(self) -> None:
        """Increase the delivery count."""
        self.__delivery_count += 1

    def remove_delivery_from_location(self, delivery_id: uuid.UUID) -> None:
        """Removes a delivery from a location, ie cancelled"""
        if not isinstance(delivery_id, uuid.UUID):
            raise exceptions.InvalidIDError()

        if delivery_id not in self.deliveries_at_location:
            raise exceptions.IDNotFoundError()

        self.__deliveries_at_location.remove(delivery_id)
        self.decrease_delivery_count()

    # [ GETTERS ] -------------------------------------------------------------

    @property
    def city(self) -> str:
        return self.__city

    @property
    def deliveries_at_location(self) -> list[uuid.UUID]:
        return self.__deliveries_at_location

    @property
    def delivery_count(self) -> int:
        return self.__delivery_count

    @property
    def location_created(self) -> datetime.datetime:
        return self.__location_created

    @property
    def location_id(self) -> str:
        return self.__location_id

    @property
    def location_name(self) -> str:
        return self.__location_name

    @property
    def location_type(self) -> str:
        return self.__location_type

    @property
    def state(self) -> str:
        return self.__state

    @property
    def street_address(self) -> str:
        return self.__street_address

    # [ SETTERS ] -------------------------------------------------------------

    @location_name.setter
    def location_name(self, new_location_name: str) -> None:
        if not validation.is_valid_location_name(new_location_name):
            raise exceptions.InvalidLocationNameError()
        self.__location_name = new_location_name

    @location_type.setter
    def location_type(self, new_location_type: str) -> None:
        if not validation.is_valid_location_type(new_location_type):
            raise exceptions.InvalidLocationTypeError()
        self.__location_type = new_location_type

    # [ DUNDERS ] -------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Location)
            and self.location_id == other.location_id
        )

    def __repr__(self) -> str:
        return f"{self.location_name} [{self.street_address}] - {self.location_type}"

    def __str__(self) -> str:
        return f"{self.__location_name}, {self.__street_address}, {self.__city} {self.__state}"
