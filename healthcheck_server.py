import threading
from flask import Flask
import sys

health_app = Flask(__name__)

@health_app.route("/", defaults={"path": ""})
@health_app.route("/<path:path>")
def health(path):
    return "OK", 200

def run_health():
    health_app.run(host="0.0.0.0", port=8000, use_reloader=False)

t = threading.Thread(target=run_health, daemon=True)
t.start()

sys.path.insert(0, "/app")
from main import main
main()
