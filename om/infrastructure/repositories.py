from om.domain.entities import FeedEvent, PondRecord
from om.infrastructure.models import FeedEvent as FeedEventModel
from om.infrastructure.models import PondRecord as PondRecordModel

"""Repository for persisting and retrieving FeedEvent entities from the database."""
class FeedEventRepository:
    @staticmethod
    def save(feed_record) -> FeedEvent:
        """
        Saves a FeedEvent entity to the database and returns the saved entity with its ID.
        """
        event = FeedEventModel.create(
            device_id   = feed_record.device_id,
            dispensed_at = feed_record.dispensed_at,
            duration    = feed_record.duration
        )
        return FeedEvent(
            feed_record.device_id,
            feed_record.dispensed_at,
            feed_record.duration,
            event.id
        )

"""Repository for persisting and retrieving PondRecord entities from the database."""
class PondRecordRepository:
    @staticmethod
    def save(pond_record) -> PondRecord:
        """
        Saves a PondRecord entity to the database and returns the saved entity with its ID.
        """
        total_records = PondRecordModel.select().count()
        if total_records >= 360:
            oldest = PondRecordModel.select().order_by(PondRecordModel.created_at.asc()).first()
            if oldest:
                oldest.delete_instance()

        record = PondRecordModel.create(
            device_id=pond_record.device_id,
            temp=pond_record.temp,
            ph=pond_record.ph,
            turbidity=pond_record.turbidity,
            created_at=pond_record.created_at
        )
        return PondRecord(
            device_id=record.device_id,
            temp=record.temp,
            ph=record.ph,
            turbidity=record.turbidity,
            created_at=record.created_at,
            id=record.id
        )