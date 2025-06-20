from datetime import timezone, datetime
from dateutil.parser import parse
from feed.domain.entities import FeedEvent

class FeedEventService:
    def __init__(self):
        pass

    @staticmethod
    def create_event(
            device_id: str,
            dispensed_at: str | None,
            duration: float,
    ) -> FeedEvent:
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