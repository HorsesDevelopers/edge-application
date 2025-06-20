from datetime import timezone, datetime
from dateutil.parser import parse
from pond.domain.entities import PondRecord

class PondRecordService:
    def __init__(self):
        pass

    @staticmethod
    def create_record(
            device_id: str,
            record_type: str,
            value: float,
            created_at: str | None
    ) -> PondRecord:

        try:
            value = float(value)
            if created_at:
                parsed_created_at = parse(created_at).astimezone(timezone.utc)
            else:
                parsed_created_at = datetime.now(timezone.utc)
        except (ValueError, TypeError):
            raise ValueError("Invalid input for BPM or created_at.")
        return PondRecord(
            device_id,
            record_type,
            value,
            parsed_created_at)