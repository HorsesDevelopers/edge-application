from datetime import datetime

class FeedEvent:
    def __init__(
            self,
            device_id: str,
            dispensed_at: datetime,
            duration: float,
            id: int = None
    ):
        self.id = id
        self.device_id = device_id
        self.dispensed_at = dispensed_at
        self.duration = duration

class PondRecord:
    def __init__(
            self,
            device_id: str,
            record_type: str,
            value: float,
            created_at: datetime,
            id: int = None
    ):
        self.id = id
        self.device_id = device_id
        self.record_type = record_type
        self.value = value
        self.created_at = created_at
