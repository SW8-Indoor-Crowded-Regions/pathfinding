import os
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

GRAPH_PATH = "app/test/mock_data/sensor_graph.pickle"
NO_PATH_GRAPH_PATH = "app/test/mock_data/no_path_sensor_graph.pickle"
MOCK_DATA_PATH = "app/test/mock_data/rooms_and_sensors.json"

@pytest.fixture
def load_mock_payload():
    with open(MOCK_DATA_PATH, "r") as f:
        return json.load(f)


def test_pathfinding_creates_pickle_if_missing(tmp_path, load_mock_payload):
    test_pickle_path = tmp_path / "sensor_graph.pickle"

    if os.path.exists(test_pickle_path):
        os.remove(test_pickle_path)

    response = client.post("/pathfinding/fastest-path", json=load_mock_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["fastest_path"] == ["67d935b5d6d3ce76bef2c962", "67d935b5d6d3ce76bef2c961"]
    assert data["distance"] == 0.3
    

def test_pathfinding_loads_pickle_if_exists(tmp_path, load_mock_payload):
    test_pickle_path = tmp_path / "sensor_graph.pickle"

    with open(GRAPH_PATH, "rb") as f:
        with open(test_pickle_path, "wb") as f2:
            f2.write(f.read())

    response = client.post("/pathfinding/fastest-path", json=load_mock_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["fastest_path"] == ["67d935b5d6d3ce76bef2c962", "67d935b5d6d3ce76bef2c961"]
    assert data["distance"] == 0.3

def test_pathfinding_handles_missing_data():
    response = client.post("/pathfinding/fastest-path", json={})
    assert response.status_code == 422

    expected_errors = [
        {
            "type": "missing",
            "loc": ["body", "source_sensor"],
            "msg": "Field required",
            "input": {}
        },
        {
            "type": "missing",
            "loc": ["body", "target_sensor"],
            "msg": "Field required",
            "input": {}
        }
    ]
    assert response.json()["detail"] == expected_errors


def test_pathfinding_handles_incorrect_source_sensor():
    response = client.post("/pathfinding/fastest-path", json={
        "rooms": [
            { "id": "67d935b5d6d3ce76bef2c962", "name": "Lobby", "crowd_factor": 2 }
        ],
        "sensors": [],
        "source_sensor": "sensor1",
        "target_sensor": "sensor2"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Source sensor 'sensor1' not found in the sensor graph."


def test_pathfinding_handles_incorrect_target_sensor():
    payload = {
        "source_sensor": "67d935b5d6d3ce76bef2c962",
        "target_sensor": "sensor2"
    }
    response = client.post("/pathfinding/fastest-path", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Target sensor 'sensor2' not found in the sensor graph."
    