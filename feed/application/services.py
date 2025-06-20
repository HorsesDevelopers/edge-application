from feed.domain.entities import FeedEvent
from feed.domain.services import FeedEventService
from feed.infrastructure.repositories import FeedEventRepository
from iam.application.services import AuthApplicationService

class FeedEventApplicationService:
    def __init__(self):
        self.feed_event_repository = FeedEventRepository()
        self.feed_event_service = FeedEventService()
        self.iam_service = AuthApplicationService()

    def create_feed_event(
            self,
            device_id: str,
            dispensed_at: str,
            duration: float,
            api_key: str
    ) -> FeedEvent:
        if not self.iam_service.get_by_id_and_api_key(device_id, api_key):
            raise ValueError("Invalid device ID or API key")
        record = self.feed_event_service.create_event(
            device_id,
            dispensed_at,
            duration
        )
        return self.feed_event_repository.save(record)