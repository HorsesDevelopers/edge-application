from datetime import timezone, datetime
from dateutil.parser import parse
from om.domain.entities import FeedEvent, PondRecord

class FeedEventService:
    """
    Domain service for creating and validating feed events.
    """
    def __init__(self):
        pass

    @staticmethod
    def create_event(
            device_id: str,
            dispensed_at: str | None,
            duration: float,
    ) -> FeedEvent:
        """
        Creates a FeedEvent entity after validating input data.
        Ensures duration is within allowed range and parses the timestamp.
        """
        try:
            duration = float(duration)
            if not (0 <= duration <= 60):
                raise ValueError("Duration must be between 0 and 60.")
            if dispensed_at:
                parsed_created_at = parse(dispensed_at).astimezone(timezone.utc)
            else:
                parsed_created_at = datetime.now(timezone.utc)
        except (ValueError, TypeError):
            raise ValueError("Invalid input for BPM or created_at.")
        return FeedEvent(
            device_id,
            parsed_created_at,
            duration,
        )

class PondRecordService:
    @staticmethod
    def create_record(
            device_id: str,
            temp: float,
            ph: float,
            turbidity: float,
            created_at: str | None,
    ) -> PondRecord:
        """
        Creates a PondRecord entity after validating input data.
        Parses the value and timestamp.
        """
        try:
            temp = float(temp)
            ph = float(ph)
            turbidity = float(turbidity)
            if created_at:
                parsed_created_at = parse(created_at).astimezone(timezone.utc)
            else:
                parsed_created_at = datetime.now(timezone.utc)
        except (ValueError, TypeError):
            raise ValueError("Invalid input for temp, ph, turbidity or created_at.")
        return PondRecord(
            device_id,
            temp,
            ph,
            turbidity,
            parsed_created_at
        )