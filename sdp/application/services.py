from sdp.domain.entities import SchedulePlaning
from sdp.domain.services import SchedulePlaningService
from sdp.infrastructure.repositories import SchedulePlaningRepository

class SchedulePlaningApplicationService:
    """
    Application service for handling schedule planning logic, including validation and persistence.
    """
    def __init__(self):
        self.domain_service = SchedulePlaningService()
        self.repository = SchedulePlaningRepository()

    def create_schedule(self, start_time: str, duration: float) -> SchedulePlaning:
        """
        Validates and creates a SchedulePlaning entity, then saves it to the repository.
        """
        schedule = self.domain_service.create_schedule(start_time, duration)
        return self.repository.save(schedule)

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