from sdp.domain.entities import SchedulePlaning
from sdp.infrastructure.models import SchedulePlaning as SchedulePlaningModel


class SchedulePlaningRepository:
    """
    Repository for persisting and retrieving SchedulePlaning entities from the database.
    """

    @staticmethod
    def save(schedule: SchedulePlaning) -> SchedulePlaning:
        """
        Saves a SchedulePlaning entity to the database and returns the saved entity with its ID.
        """
        model = SchedulePlaningModel.create(
            start_time=schedule.start_time,
            duration=schedule.duration
        )
        return SchedulePlaning(
            start_time=model.start_time,
            duration=model.duration,
            id=model.id
        )

    @staticmethod
    def get_all() -> list[SchedulePlaning]:
        """
        Retrieves all schedules from the database.
        """
        schedules = []
        for s in SchedulePlaningModel.select():
            schedules.append(SchedulePlaning(
                start_time=s.start_time,
                duration=s.duration,
                id=s.id
            ))
        return schedules

    @staticmethod
    def delete_by_id(schedule_id: int) -> bool:
        """
        Deletes a schedule by its ID. Returns True if deleted, False if not found.
        """
        deleted = SchedulePlaningModel.delete().where(SchedulePlaningModel.id == schedule_id).execute()
        return deleted > 0