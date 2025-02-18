import datetime
import uuid
from helpers import utils, exceptions, reference
from models.location import Location


class DeliveryStep:
    """Represents a step in the delivery chain and contains a Location, as well as current data for that particular delivery."""

    def __init__(
        self,
        shift_id: uuid.UUID,
        delivery_id: uuid.UUID,
        location: Location,
        previous_odometer_reading: int,
        current_odometer_reading: int,
        order_count: int,
    ) -> None:
        self.__delivery_step_id = utils.generate_id()
        self.__shift_id: uuid.UUID = shift_id
        self.__delivery_id: uuid.UUID = delivery_id
        self.__location: Location = location
        self.__previous_odometer_reading: int = previous_odometer_reading
        self.__current_odometer_reading: int = current_odometer_reading
        self.__number_of_miles: int = self.__calculate_mileage()
        self.__order_count: int = order_count
        self.__creation_timestamp: datetime.datetime = utils.get_timestamp()
        self.__arrival_timestamp: datetime.datetime | None = None
        self.__departure_timestamp: datetime.datetime | None = None
        self.__duration: datetime.timedelta | None = None
        self.__status: str = "Not Started"

    # [ METHODS ] -------------------------------------------------------------

    def adjust_current_odometer_reading(self, new_reading: int) -> None:
        """Adjusts the odometer reading for the delivery step"""
        if new_reading < self.__previous_odometer_reading:
            raise exceptions.InvalidOdometerReading(
                f"The odometer reading({new_reading}) cannot be less than the previous odometer reading."
            )

        self.__current_odometer_reading = new_reading
        self.__number_of_miles = self.__calculate_mileage()

    def __calculate_duration(self) -> None:
        """Calculates the duration if both the arrival and departure timestamps are set."""
        if (
            self.__departure_timestamp is not None
            and self.__arrival_timestamp is not None
        ):
            self.__duration = (
                self.__departure_timestamp - self.__arrival_timestamp
            )

    def __calculate_mileage(self) -> int:
        """Calculates the mileage based on odometer readings."""
        return (
            self.__current_odometer_reading - self.__previous_odometer_reading
        )

    def decrease_order_count(self) -> None:
        """Decrease the order count by one."""
        if self.__order_count >= 1:
            self.__order_count -= 1

    def increase_order_count(self) -> None:
        """Increase the order count by one."""
        self.__order_count += 1

    def reset_timestamps(self) -> None:
        """Resets the arrival and departure timestamps, as well as the duration."""
        self.__arrival_timestamp = None
        self.__departure_timestamp = None
        self.__duration = None
        self.__status = "Not Started"

    def set_arrival_timestamp(self) -> None:
        """Sets a timestamp for the arrival time."""
        self.__arrival_timestamp = utils.get_timestamp()
        self.__set_status("In Progress")

    def set_departure_timestamp(self) -> None:
        """Sets a timestamp for the departure time."""
        self.__departure_timestamp = utils.get_timestamp()
        self.__calculate_duration()
        self.__set_status("Complete")

    def __set_status(self, status: str) -> None:
        """Sets the status of the DeliveryStep."""
        if status not in reference.delivery_step_statuses:
            raise exceptions.InvalidDeliveryStepStatusError(
                f"'{status}' is not a valid Delivery Step status."
            )

        self.__status = status

    # [ GETTERS ] -------------------------------------------------------------

    @property
    def delivery_step_id(self) -> uuid.UUID:
        return self.__delivery_step_id

    @property
    def shift_id(self) -> uuid.UUID:
        return self.__shift_id

    @property
    def delivery_id(self) -> uuid.UUID:
        return self.__delivery_id

    @property
    def location(self) -> Location:
        return self.__location

    @property
    def previous_odometer_reading(self) -> int:
        return self.__previous_odometer_reading

    @property
    def current_odometer_reading(self) -> int:
        return self.__current_odometer_reading

    @property
    def number_of_miles(self) -> int:
        return self.__number_of_miles

    @property
    def order_count(self) -> int:
        return self.__order_count

    @property
    def creation_timestamp(self) -> datetime.datetime:
        return self.__creation_timestamp

    @property
    def arrival_timestamp(self) -> datetime.datetime | None:
        return self.__arrival_timestamp

    @property
    def departure_timestamp(self) -> datetime.datetime | None:
        return self.__departure_timestamp

    @property
    def duration(self) -> datetime.timedelta | None:
        return self.__duration

    @property
    def status(self) -> str:
        return self.__status

    # [ SETTERS ] -------------------------------------------------------------

    @current_odometer_reading.setter
    def current_odometer_reading(self, new_reading: int) -> None:
        if new_reading < self.__previous_odometer_reading:
            raise exceptions.InvalidOdometerReading(
                f"Odometer reading ({new_reading}) cannot be less than the previous odometer reading ({self.__previous_odometer_reading})."
            )
        self.__current_odometer_reading = new_reading
        self.__number_of_miles = self.__calculate_mileage()

    # [ DUNDERS ] -------------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        return bool(
            isinstance(other, DeliveryStep)
            and self.delivery_id == other.delivery_id
        )

    def __str__(self) -> str:
        string = f"{self.location.location_name}"
        string += f"({self.location.street_address})\n"
        if self.status == "Not Started":
            string += f"Status: {self.status}"
        elif self.status == "In Progress":
            string += f"Arrived: {self.arrival_timestamp.hour}:"
            string += f"{self.arrival_timestamp.minute}"
        elif self.status == "Complete":
            string += f"Arrived: {self.arrival_timestamp.hour}:"
            string += f"{self.arrival_timestamp.minute} "
            string += f"Departed: {self.departure_timestamp.hour}:"
            string += f"{self.departure_timestamp.minute}"

        return string
