from flask import Blueprint, request, jsonify, Response

from iam.application.services import AuthApplicationService

iam_api = Blueprint('iam_api', __name__)

auth_service = AuthApplicationService()

def authenticate_request() -> None | tuple[Response, int]:
    device_id   = request.json.get('device_id') if request.json else None
    api_key     = request.headers.get('X-API-Key')
    if not device_id or not api_key:
        return jsonify({"error": "Device ID and API key are required"}), 401
    if not auth_service.authenticate(device_id, api_key):
        return jsonify({"error": "Invalid device_id or API key"}), 401
    return None

@iam_api.route('/devices', methods=['POST'])
def create_or_update_device():
    data = request.json
    device_id = data.get('device_id')
    api_key = data.get('api_key')
    if not device_id or not api_key:
        return jsonify({"error": "device_id y api_key requeridos"}), 400

    device = auth_service.create_or_update_device(device_id, api_key)
    return jsonify({"device_id": device.device_id, "api_key": device.api_key}), 200