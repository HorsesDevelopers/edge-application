from flask import Flask

import iam.application.services
from iam.interfaces.services import iam_api
from om.interfaces.services import feed_api, pond_api

from shared.infrastructure.database import init_db

app = Flask(__name__)

app.register_blueprint(iam_api)
app.register_blueprint(pond_api)

app.register_blueprint(feed_api)
first_request = True

@app.before_request
def setup():
    global first_request
    if first_request:
        first_request = False
        init_db()
        auth_application_service = iam.application.services.AuthApplicationService()
        auth_application_service.get_or_create_test_device()

def forward_records():
    feed_url = "http://localhost:5000/api/v1/feed-deployment/data-events/recent"
    pond_url = "http://localhost:5000/api/v1/pond-monitoring/data-records/recent"
    spring_url_feed = "http://localhost:8080/api/feed"
    spring_url_pond = "http://localhost:8080/api/pond"

    feed_events = requests.get(feed_url).json()
    pond_records = requests.get(pond_url).json()

    if feed_events:
        requests.post(spring_url_feed, json=feed_events)
    if pond_records:
        requests.post(spring_url_pond, json=pond_records)

import threading
import time
import requests

DEVICE_ID = "pond-001"
DEVICE_URL = "http://192.168.234.242/data"
FOG_URL = "http://localhost:8080/fog1/v1/edge-data"  # Asegúrate que este endpoint esté activo

def poll_and_forward():
    while True:
        try:
            print("Haciendo GET al device...")
            resp = requests.get(DEVICE_URL, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            data["device_id"] = DEVICE_ID
            print("Payload a enviar al fog:", data)
            fog_resp = requests.post(FOG_URL, json=data, timeout=5)
            print("Respuesta del fog:", fog_resp.status_code, fog_resp.text)
            fog_resp.raise_for_status()
            print("Enviado al fog correctamente.")
        except Exception as e:
            print("Error en poll_and_forward:", e)
        time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=poll_and_forward, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)