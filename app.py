from flask import Flask, jsonify
import os

app = Flask(__name__)

LOG_FILE = os.getenv("LOG_FILE", "app.log")


@app.route("/")
def home():
    return jsonify({
        "service": "platform-log-service",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/logs")
def logs():
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()

        errors = [line.strip() for line in lines if "ERROR" in line]

        return jsonify({
            "error_count": len(errors),
            "errors": errors
        })

    except FileNotFoundError:
        return jsonify({
            "error": f"Log file '{LOG_FILE}' not found"
        }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
