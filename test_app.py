import app
import pytest


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary file instead of real appointment data
    test_data_file = tmp_path / "appointments.json"

    monkeypatch.setattr(app, "DATA_FILE", str(test_data_file))
    monkeypatch.setattr(app, "appointments", [])
    monkeypatch.setattr(app, "next_id", 1)

    app.app.config["TESTING"] = True

    with app.app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["application"] == "Cloud Hospital"
    assert response.json["status"] == "online"


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_appointments(client):
    response = client.get("/appointments")

    assert response.status_code == 200
    assert response.json == []


def test_create_appointment(client):
    response = client.post(
        "/appointments",
        json={
            "patient": "Test Patient",
            "doctor": "Dr. Sharma",
            "date": "2026-11-10"
        }
    )

    assert response.status_code == 201
    assert response.json["appointment"]["patient"] == "Test Patient"
    assert response.json["appointment"]["doctor"] == "Dr. Sharma"


def test_create_appointment_missing_fields(client):
    response = client.post(
        "/appointments",
        json={
            "patient": "Test Patient"
        }
    )

    assert response.status_code == 400
    assert "error" in response.json
