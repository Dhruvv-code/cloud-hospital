import json
from flask import Flask, request, jsonify
from datetime import datetime, timezone
import os

app = Flask(__name__)

DATA_FILE = "/app/data/appointments.json"

os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)


def load_appointments():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_appointments():
    with open(DATA_FILE, "w") as file:
        json.dump(appointments, file, indent=4)


appointments = load_appointments()

next_id = max(
    (appointment["id"] for appointment in appointments),
    default=0
) + 1


@app.route("/")
def home():
    return jsonify({
        "application": "Cloud Hospital",
        "message": "Hospital Appointment System is running",
        "status": "online"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "Cloud Hospital",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200


@app.route("/appointments", methods=["GET"])
def get_appointments():
    return jsonify(appointments), 200


@app.route("/appointments", methods=["POST"])
def create_appointment():
    global next_id

    data = request.get_json(silent=True) or {}

    patient = data.get("patient")
    doctor = data.get("doctor")
    date = data.get("date")

    if not patient or not doctor or not date:
        return jsonify({
            "error": "patient, doctor and date are required"
        }), 400

    appointment = {
        "id": next_id,
        "patient": patient,
        "doctor": doctor,
        "date": date
    }

    appointments.append(appointment)
    save_appointments()
    next_id +=1

    return jsonify({
        "message": "Appointment created successfully",
        "appointment": appointment
    }), 201


if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port, debug=False)
