import json
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

MOCK_DATA_PATH = 'app/test/mock_data/rooms_and_sensors.json'
MOCK_DATA_NO_PATH = 'app/test/mock_data/rooms_and_sensors_no_path.json'


@pytest.fixture
def load_mock_payload():
    with open(MOCK_DATA_PATH, 'r') as f:
        return json.load(f)

@pytest.fixture
def load_no_path_mock_payload():
    with open(MOCK_DATA_NO_PATH, 'r') as f:
        return json.load(f)

def test_pathfinding_returns_correct_path(load_mock_payload):
    response = client.post('/pathfinding/fastest-path', json=load_mock_payload)

    assert response.status_code == 200
    data = response.json()
    assert data['fastest_path'] == [{'id': '67d935b5d6d3ce76bef2c960', 'longitude': 10.857185147851341, 'latitude': 11.032101366333102}, {'id': '67d935b5d6d3ce76bef2c95a', 'longitude': 47.31982729135278, 'latitude': 42.8210378030866}, {'id': '67d935b5d6d3ce76bef2c961', 'longitude': 64.81348685573096, 'latitude': 20.355786846137036}]
    assert data['distance'] == 0.342


def test_pathfinding_handles_missing_data():
    response = client.post('/pathfinding/fastest-path', json={})
    assert response.status_code == 422

    expected_errors = [
        {'type': 'missing', 'loc': ['body', 'rooms'], 'msg': 'Field required', 'input': {}},
        {'type': 'missing', 'loc': ['body', 'sensors'], 'msg': 'Field required', 'input': {}},
        {'type': 'missing', 'loc': ['body', 'source_sensor'], 'msg': 'Field required', 'input': {}},
        {'type': 'missing', 'loc': ['body', 'target_sensor'], 'msg': 'Field required', 'input': {}},
    ]
    assert response.json()['detail'] == expected_errors


def test_pathfinding_handles_incorrect_source_sensor(load_mock_payload):
    payload = load_mock_payload
    payload['source_sensor'] = 'non_existent_sensor'
    response = client.post(
        '/pathfinding/fastest-path',
        json=payload,
    )
    assert response.status_code == 400
    assert response.json()['detail'] == "Source sensor 'non_existent_sensor' not found in the sensor graph."


def test_pathfinding_handles_incorrect_target_sensor(load_mock_payload):
    payload = load_mock_payload
    payload['target_sensor'] = 'non_existent_sensor'
    response = client.post('/pathfinding/fastest-path', json=payload)
    assert response.status_code == 400
    assert response.json()['detail'] == "Target sensor 'non_existent_sensor' not found in the sensor graph."
    
def test_pathfinding_handles_no_path(load_no_path_mock_payload):
    response = client.post('/pathfinding/fastest-path', json=load_no_path_mock_payload)
    assert response.status_code == 400
    assert response.json()['detail'] == 'No path found between the given sensors.'
    