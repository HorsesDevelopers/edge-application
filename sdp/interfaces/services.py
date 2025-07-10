from flask import Blueprint, request, jsonify
from sdp.application.services import SchedulePlaningApplicationService

schedule_api = Blueprint("schedule_api", __name__)
schedule_service = SchedulePlaningApplicationService()

@schedule_api.route("/api/v1/schedule", methods=["POST"])
def create_schedule():
    """
    Endpoint para crear un nuevo schedule.
    Espera start_time (ISO 8601) y duration (float) en el body.
    """
    data = request.json
    try:
        start_time = data["start_time"]
        duration = data["duration"]
        schedule = schedule_service.create_schedule(start_time, duration)
        return jsonify({
            "id": schedule.id,
            "start_time": schedule.start_time.isoformat(),
            "duration": schedule.duration
        }), 201
    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@schedule_api.route("/api/v1/schedules", methods=["GET"])
def get_schedules():
    """
    Endpoint para obtener todos los schedules.
    """
    schedules = schedule_service.get_schedules()
    return jsonify([
        {
            "id": s.id,
            "start_time": s.start_time.isoformat(),
            "duration": s.duration
        } for s in schedules
    ])

@schedule_api.route("/api/v1/schedules/<int:schedule_id>", methods=["DELETE"])
def delete_schedule(schedule_id):
    """
    Endpoint para eliminar un schedule por su ID.
    """
    deleted = schedule_service.delete_schedule(schedule_id)
    if deleted:
        return jsonify({"message": "Schedule deleted"}), 200
    else:
        return jsonify({"error": "Schedule not found"}), 404