import uuid


class DeliveryManager:
    """Manages all aspects of deliveries."""

    def __init__(self) -> None:
        self.deliveries: dict[uuid.uuid4, object] = {}
        self.delivery_steps: dict[uuid.uuid4, object] = {}
        self.locations: dict[uuid.uuid4, object] = {}
