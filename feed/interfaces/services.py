from flask import Blueprint, request, jsonify
from feed.application.services import FeedEventApplicationService
from iam.interfaces.services import authenticate_request

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

