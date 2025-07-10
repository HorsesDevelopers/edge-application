from sdp.domain.entities import SchedulePlaning
from datetime import datetime
from sdp.infrastructure.repositories import SchedulePlaningRepository

class SchedulePlaningService:
    """
    Service for managing schedule planning operations.
    """
    def __init__(self):
        self.repository = SchedulePlaningRepository()

    @staticmethod
    def create_schedule(
            start_time: str,
            duration: float,
            id: int = None
    ) -> SchedulePlaning:
        """
        Creates a SchedulePlaning entity after validating input data.
        Parses the start time and ensures duration is within allowed range.
        """
        try:
            duration = float(duration)
            if not (0 <= duration <= 3600):
                raise ValueError("Duration must be between 0 and 3600 seconds.")
            parsed_start_time = datetime.fromisoformat(start_time).astimezone()
        except (ValueError, TypeError):
            raise ValueError("Invalid input for start_time or duration.")

        return SchedulePlaning(
            start_time=parsed_start_time,
            duration=duration,
            id=id
        )

    def get_schedules(self) -> list[SchedulePlaning]:
        """
        Retrieves all schedules from the repository.
        """
        return self.repository.get_all()

    def delete_schedule(self, schedule_id: int) -> bool:
        """
        Deletes a schedule by its ID.
        Returns True if deleted, False if not found.
        """
        return self.repository.delete_by_id(schedule_id)