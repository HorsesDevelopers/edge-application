from datetime import datetime

class SchedulePlaning:
    """
    Domain entity representing a schedule for planning events.
    Stores the device ID, the start and end times of the schedule, and the duration.
    """
    def __init__(
            self,
            start_time: datetime,
            duration: float,
            id: int = None
    ):
        self.id = id  # Unique identifier for the schedule (optional)
        self.start_time = start_time  # Start time of the schedule
        self.duration = duration  # Duration of the scheduled event in seconds