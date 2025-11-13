from flask import Flask, jsonify
import os
import socket
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    app_name = os.getenv("APP_NAME", "DevOps Python App")
    return jsonify({
        "message": f"{app_name} is running successfully!",
        "host": socket.gethostname(),
        "time": datetime.datetime.now().isoformat()
    })

@app.route("/health")
def health():
    return jsonify({"status": "UP"}), 200

@app.route("/version")
def version():
    return jsonify({
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development")
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
