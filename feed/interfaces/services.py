from flask import Blueprint, request, jsonify
from feed.application.services import FeedEventApplicationService
from iam.interfaces.services import authenticate_request
from datetime import datetime, timedelta, timezone
from feed.infrastructure.models import FeedEvent as FeedEventModel
from dateutil.parser import parse
feed_api = Blueprint("feeed_api", __name__)

feed_event_service = FeedEventApplicationService()

@feed_api.route("/api/v1/feed-deployment/data-events", methods=["POST"])
def create_feed_event():
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