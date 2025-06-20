from feed.domain.entities import FeedEvent
from feed.infrastructure.models import FeedEvent as FeedEventModel

class FeedEventRepository:

    @staticmethod
    def save(feed_record) -> FeedEvent:

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