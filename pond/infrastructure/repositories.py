from pond.domain.entities import PondRecord
from pond.infrastructure.models import PondRecord as PondRecordModel

class PondRecordRepository:
    @staticmethod
    def save(pond_record) -> PondRecord:
        record = PondRecordModel.create(
            device_id   = pond_record.device_id,
            record_type = pond_record.record_type,
            value       = pond_record.value,
            created_at  = pond_record.created_at
        )
        return PondRecord(
            id          = record.id,
            device_id   = record.device_id,
            record_type = record.record_type,
            value       = record.value,
            created_at  = record.created_at
        )