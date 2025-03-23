import eventlet
eventlet.monkey_patch()  # 🛠️ Apply monkey patching before importing anything else

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from monitor import SiteMonitor
from datetime import datetime


app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

# Initialize the SiteMonitor class
monitor = SiteMonitor(socketio)

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("start_monitoring")
def start_monitoring(data):
    """Handles a request to start monitoring a site."""
    url = data.get("url")

    if not url:
        emit("error", {"message": "Invalid URL provided"})
        return

    try:
        monitor.monitor_site(url)
        # Send an initial status update
        emit("status_update", {"sites": monitor.sites}, broadcast=True)
    except Exception as e:
        emit("error", {"message": f"Failed to start monitoring: {str(e)}"})

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000)
