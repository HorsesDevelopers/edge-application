from pond.domain.entities import PondRecord
from pond.infrastructure.models import PondRecord as PondRecordModel
from datetime import datetime

class PondRecordRepository:
    @staticmethod
    def save(pond_record) -> PondRecord:
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