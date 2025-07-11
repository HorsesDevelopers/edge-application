from typing import Optional
from iam.domain.entities import Device
from iam.domain.services import AuthService
from iam.infrastructure.repositories import DeviceRepository
from iam.infrastructure.models import Device as DeviceModel
from datetime import datetime


class AuthApplicationService:
    def __init__(self):
        self.device_repository = DeviceRepository()
        self.auth_service = AuthService()

    def authenticate(self, device_id: str, api_key: str):

        device: Optional[Device] = self.device_repository.find_by_id_and_api_key(device_id, api_key)
        return self.auth_service.authenticate(device)

    def get_by_id_and_api_key(self, device_id: str, api_key: str) -> Optional[Device]:
        return self.device_repository.find_by_id_and_api_key(device_id, api_key)

    def get_or_create_test_device(self) -> Device:

        return self.device_repository.get_or_create_test_device()

    def create_or_update_device(self, device_id: str, api_key: str) -> Optional[Device]:
        if not device_id or not api_key:
            return None
        device_model, created = DeviceModel.get_or_create(
            device_id=device_id,
            defaults={"api_key": api_key, "created_at": datetime.utcnow()}
        )
        if not created:
            device_model.api_key = api_key
            device_model.save()
        device = Device(device_model.device_id, device_model.api_key, device_model.created_at)
        return self.device_repository.save(device)