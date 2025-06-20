from pond.domain.entities import PondRecord
from pond.domain.services import PondRecordService
from pond.infrastructure.repositories import PondRecordRepository
from iam.application.services import AuthApplicationService

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