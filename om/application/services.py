from om.domain.entities import FeedEvent, PondRecord
from om.domain.services import FeedEventService, PondRecordService
from om.infrastructure.repositories import FeedEventRepository, PondRecordRepository
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


class PondRecordApplicationService:
    def __init__(self):
        self.pond_record_repository = PondRecordRepository()
        self.pond_record_service = PondRecordService()
        self.iam_service = AuthApplicationService()

    def create_pond_record(
            self,
            device_id: str,
            record_type: str,
            value: float,
            created_at: str,
            api_key: str
    ) -> PondRecord:
        if not self.iam_service.get_by_id_and_api_key(
                device_id, api_key):
            raise ValueError("Invalid device ID or API key")
        record = self.pond_record_service.create_record(
            device_id,
            record_type,
            value,
            created_at
        )
        return self.pond_record_repository.save(record)