import os
import json
import secrets
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

REPORT_FILE = Path(__file__).resolve().parent / "reports" / "test-report.json"
REPORT_TOKEN = os.environ.get("REPORT_TOKEN")


@app.route("/report", methods=["POST"])
def receive_report():
    if not REPORT_TOKEN:
        return jsonify({"error": "Receiver token is not configured"}), 500

    received_token = request.headers.get("X-Report-Token", "")

    if not secrets.compare_digest(received_token, REPORT_TOKEN):
        return jsonify({"error": "Unauthorized"}), 401

    report = request.get_json(silent=True)

    if not isinstance(report, dict):
        return jsonify({"error": "Invalid JSON report"}), 400

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    temporary_file = REPORT_FILE.with_suffix(".tmp")
    temporary_file.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8"
    )
    temporary_file.replace(REPORT_FILE)

    print(f"Report received and saved: {REPORT_FILE}")

    return jsonify({
        "message": "Report received successfully",
        "file": str(REPORT_FILE)
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Receiver is running"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
