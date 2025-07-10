from flask import Blueprint, request, jsonify
from om.application.services import PondRecordApplicationService
from om.application.services import FeedEventApplicationService
from iam.interfaces.services import authenticate_request
from datetime import datetime, timedelta, timezone
from om.infrastructure.models import FeedEvent as FeedEventModel
from om.infrastructure.models import PondRecord as PondRecordModel
from dateutil.parser import parse
feed_api = Blueprint("feed_api", __name__)
pond_api = Blueprint("pond_api", __name__)

pond_record_service = PondRecordApplicationService()
feed_event_service = FeedEventApplicationService()

@feed_api.route("/api/v1/feed-deployment/data-events", methods=["POST"])
def create_feed_event():
    """
    Endpoint to create a new feed event.
    Expects device ID, dispensed_at timestamp, and duration in the request body.
    Requires a valid API key in the headers.
    Returns the created feed event or an error message.
    """
    auth_result = authenticate_request()
    if auth_result:
        return auth_result
    data = request.json
    try:
        device_id = data["device_id"]
        dispensed_at = data.get("dispensed_at")
        duration = data.get("duration")
        event = feed_event_service.create_feed_event(
            device_id,
            dispensed_at,
            duration,
            request.headers.get("X-API-Key")
        )
        return jsonify({
            "id": event.id,
            "device_id": event.device_id,
            "dispensed_at": event.dispensed_at.isoformat() + "Z",
            "duration": event.duration,
        }), 201
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@feed_api.route("/api/v1/feed-deployment/data-events/recent", methods=["GET"])
def get_recent_feed_events():
    """
    Endpoint to retrieve recent feed events from the last 10 minutes.
    Returns a list of feed events with their details.
    """
    since = datetime.now(timezone.utc) - timedelta(minutes=10)
    events = FeedEventModel.select().where(FeedEventModel.dispensed_at >= since)
    return jsonify([
        {
            "id": e.id,
            "device_id": e.device_id,
            "dispensed_at": parse(e.dispensed_at).isoformat() + "Z" if isinstance(e.dispensed_at, str) else e.dispensed_at.isoformat() + "Z",
            "duration": e.duration
        } for e in events
    ])

@pond_api.route("/api/v1/pond-monitoring/data-records/batch", methods=["POST"])
def create_pond_records_batch():
    """
    Receives temp, turbidity and ph together and saves them as separate records.
    """
    auth_result = authenticate_request()
    if auth_result:
        return auth_result
    data = request.json
    try:
        device_id = data["device_id"]
        created_at = data.get("created_at")
        temp = data.get("temp")
        ph = data.get("ph")
        turbidity = data.get("turbidity")
        api_key = request.headers.get("X-API-Key")

        if temp is None or ph is None or turbidity is None:
            return jsonify({"error": "temp, ph y turbidity son requeridos"}), 400

        record = pond_record_service.create_pond_record(
            device_id,
            temp,
            ph,
            turbidity,
            created_at,
            api_key,
        )
        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "temp": record.temp,
            "ph": record.ph,
            "turbidity": record.turbidity,
            "created_at": record.created_at.isoformat() + "Z"
        }), 201
    except KeyError:
        return jsonify({"error": "Missing fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@pond_api.route("/api/v1/pond-monitoring/data-records/recent", methods=["GET"])
def get_recent_pond_records():
    """
    Endpoint to retrieve recent pond sensor records from the last 10 minutes.
    Returns a list of pond records with their details.
    """
    since = datetime.now(timezone.utc) - timedelta(minutes=10)
    records = PondRecordModel.select().where(PondRecordModel.created_at >= since)
    return jsonify([
        {
            "id": r.id,
            "device_id": r.device_id,
            "record_type": r.record_type,
            "value": r.value,
            "created_at": parse(r.created_at).isoformat() + "Z" if isinstance(r.created_at, str) else r.created_at.isoformat() + "Z"
        } for r in records
    ])