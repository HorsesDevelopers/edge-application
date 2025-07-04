from om.domain.entities import FeedEvent, PondRecord
from om.infrastructure.models import FeedEvent as FeedEventModel
from om.infrastructure.models import PondRecord as PondRecordModel
from datetime import datetime

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
        record = PondRecordModel.create(
            device_id   = pond_record.device_id,
            record_type = pond_record.record_type,
            value       = pond_record.value,
            created_at  = pond_record.created_at
        )
        created_at = record.created_at
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        return PondRecord(
            id          = record.id,
            device_id   = record.device_id,
            record_type = record.record_type,
            value       = record.value,
            created_at  = record.created_at
        )