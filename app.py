from flask import Flask
import threading
from sdp.interfaces import services
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

if __name__ == "__main__":
    mqtt_thread = threading.Thread(target=services.main, daemon=True)
    mqtt_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)