from om.domain.entities import FeedEvent, PondRecord
from om.domain.services import FeedEventService, PondRecordService
from om.infrastructure.repositories import FeedEventRepository, PondRecordRepository
from om.domain.entities import PondRecord
from om.domain.services import PondRecordService
from om.infrastructure.repositories import PondRecordRepository
from iam.application.services import AuthApplicationService
from typing import Optional
from om.infrastructure.models import PondRecord as PondRecordModel

import time
import requests


"""Service for handling feed event application logic, including validation and persistence. """
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
    ) -> Optional[FeedEvent]:
        """
        Validates the device and API key, creates a FeedEvent entity, and saves it to the repository.
        """
        if not self.iam_service.get_by_id_and_api_key(device_id, api_key):
            raise ValueError("Invalid device ID or API key")
        record = self.feed_event_service.create_event(
            device_id,
            dispensed_at,
            duration
        )
        return self.feed_event_repository.save(record)

"""Service for handling pond record application logic, including validation and persistence."""
class PondRecordApplicationService:
    def __init__(self):
        self.pond_record_repository = PondRecordRepository()
        self.pond_record_service = PondRecordService()
        self.iam_service = AuthApplicationService()
        self.last_sent_to_fog = {}  # device_id -> timestamp

    def create_pond_record(
            self,
            device_id: str,
            temp: float,
            ph: float,
            turbidity: float,
            created_at: str,
            api_key: str,
    ) -> Optional[PondRecord]:
        if not self.iam_service.get_by_id_and_api_key(device_id, api_key):
            raise ValueError("Invalid device ID or API key")

        last = PondRecordModel.select().where(PondRecordModel.device_id == device_id).order_by(PondRecordModel.created_at.desc()).first()
        threshold_temp = 2.0
        threshold_ph = 0.5
        threshold_turbidity = 5.0
        should_notify = False
        if last:
            if abs(float(temp) - last.temp) > threshold_temp:
                should_notify = True
            if abs(float(ph) - last.ph) > threshold_ph:
                should_notify = True
            if abs(float(turbidity) - last.turbidity) > threshold_turbidity:
                should_notify = True

        # Chequear si pasaron 5 minutos desde el último envío
        now = time.time()
        last_sent = self.last_sent_to_fog.get(device_id, 0)
        five_minutes = 5 * 60
        if now - last_sent >= five_minutes:
            should_notify = True

        record = self.pond_record_service.create_record(
            device_id,
            temp,
            ph,
            turbidity,
            created_at,
        )
        saved_record = self.pond_record_repository.save(record)

        if should_notify:
            try:
                requests.post(
                    "http://localhost:8081/api/v1/ponds_record",
                    json={
                        "pondId": 1,
                        "temp": temp,
                        "ph": ph,
                        "turbidity": turbidity
                    },
                    timeout=2
                )
                self.last_sent_to_fog[device_id] = now
            except Exception as e:
                print(f"Error notificando al fog: {e}")

        return saved_record