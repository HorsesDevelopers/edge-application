from flask import Blueprint, request, jsonify
from pond.application.services import PondRecordApplicationService
from iam.interfaces.services import authenticate_request

pond_api = Blueprint("pond_api", __name__)

health_record_service = PondRecordApplicationService()

@pond_api.route("/api/v1/pond-monitoring/data-records", methods=["POST"])
def create_health_record():
    auth_result = authenticate_request()
    if auth_result:
        return auth_result
    data = request.json
    try:
        device_id = data["device_id"]
        record_type = data["record_type"]
        value = data["value"]
        created_at = data.get("created_at")
        record = health_record_service.create_pond_record(
            device_id,
            record_type,
            value,
            created_at,
            request.headers.get("X-API-Key")
        )
        return jsonify({
            "id": record.id,
            "device_id": record.device_id,
            "record_type": record.record_type,
            "value": record.value,
            "created_at": record.created_at.isoformat() + "Z"
        }), 201
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

