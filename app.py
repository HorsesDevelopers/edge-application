from flask import Flask

import time
import requests
import iam.application.services
from pond.interfaces.services import pond_api
from iam.interfaces.services import iam_api
from feed.interfaces.services import feed_api

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
    while True:
        forward_records()
        time.sleep(600)  # 10 minutos
