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
	assert 'fastest_path' in data
	assert 'distance' in data
	assert data['fastest_path'] == [
		{
			'id': '67d935b1d6d3ce76bef2c8e9',
			'longitude': 16.369509547137667,
			'latitude': 23.8621854675587,
		},
		{
			'id': '67d935b1d6d3ce76bef2c8ea',
			'longitude': 61.74727469899295,
			'latitude': 72.87442522121299,
		},
	]
	assert data['distance'] == 0.09


def test_pathfinding_handles_missing_data():
	response = client.post('/pathfinding/fastest-path', json={})
	assert response.status_code == 422

	expected_errors = [
		{'type': 'missing', 'loc': ['body', 'rooms'], 'msg': 'Field required', 'input': {}},
		{'type': 'missing', 'loc': ['body', 'sensors'], 'msg': 'Field required', 'input': {}},
		{'type': 'missing', 'loc': ['body', 'source_room'], 'msg': 'Field required', 'input': {}},
		{'type': 'missing', 'loc': ['body', 'target_room'], 'msg': 'Field required', 'input': {}},
	]
	assert response.json()['detail'] == expected_errors


def test_pathfinding_handles_incorrect_source_room(load_mock_payload):
	payload = load_mock_payload
	payload['source_room'] = 'non_existent_room'
	response = client.post(
		'/pathfinding/fastest-path',
		json=payload,
	)
	assert response.status_code == 400
	assert (
		response.json()['detail']
		== "Source room 'non_existent_room' is not valid."
	)


def test_pathfinding_handles_incorrect_target_room(load_mock_payload):
	payload = load_mock_payload
	payload['target_room'] = 'non_existent_sensor'
	response = client.post('/pathfinding/fastest-path', json=payload)
	assert response.status_code == 400
	assert (
		response.json()['detail']
		== "Target room 'non_existent_sensor' is not valid."
	)


def test_pathfinding_handles_no_path(load_no_path_mock_payload):
	response = client.post('/pathfinding/fastest-path', json=load_no_path_mock_payload)
	assert response.status_code == 400
	assert response.json()['detail'] == 'No path found between the given rooms.'
