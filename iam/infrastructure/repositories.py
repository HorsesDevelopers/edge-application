import peewee
from typing import Optional
from iam.domain.entities import Device
from iam.infrastructure.models import Device as DeviceModel

class DeviceRepository:
    @staticmethod
    def find_by_id_and_api_key(device_id: str, api_key: str) -> Optional[Device]:
        try:
            device = DeviceModel.get((DeviceModel.device_id == device_id) & (DeviceModel.api_key == api_key))
            return Device(device.device_id, device.api_key, device.created_at)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def get_or_create_test_device() -> Device:
        device, _ = DeviceModel.get_or_create(
            device_id='pond-001',
            defaults={"api_key": "test-api-key-123", "created_at": "2025-06-06T12:00:00Z"})
        return Device(device.device_id, device.api_key, device.created_at)

    @staticmethod
    def save(device: Device) -> Device:
        device_model, _ = DeviceModel.get_or_create(
            device_id=device.device_id,
            defaults={"api_key": device.api_key, "created_at": device.created_at}
        )
        device_model.api_key = device.api_key
        device_model.created_at = device.created_at
        device_model.save()
        return Device(device_model.device_id, device_model.api_key, device_model.created_at)