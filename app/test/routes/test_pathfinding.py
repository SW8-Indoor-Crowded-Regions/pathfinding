import json
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

MOCK_DATA_PATH = 'app/test/mock_data/rooms_and_sensors.json'
MOCK_DATA_NO_PATH = 'app/test/mock_data/rooms_and_sensors_no_path.json'
MULTIPLE_POINTS_PATH = 'app/test/mock_data/multiple_points.json'


@pytest.fixture
def load_mock_payload():
	with open(MOCK_DATA_PATH, 'r') as f:
		return json.load(f)


@pytest.fixture
def load_no_path_mock_payload():
	with open(MOCK_DATA_NO_PATH, 'r') as f:
		return json.load(f)


@pytest.fixture
def load_multiple_points_payload():
	with open(MULTIPLE_POINTS_PATH, 'r') as f:
		return json.load(f)


def test_pathfinding_returns_correct_path(load_mock_payload):
	response = client.post('/pathfinding/fastest-path', json=load_mock_payload)

	assert response.status_code == 200
	data = response.json()
	assert 'fastest_path' in data
	assert 'distance' in data
	assert isinstance(data['fastest_path'], list)
	assert isinstance(data['distance'], (int, float))
	assert all(isinstance(sensor, dict) for sensor in data['fastest_path'])
	assert isinstance(data['distance'], (int, float))


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
	assert response.json()['detail'] == "Source room 'non_existent_room' is not valid."


def test_pathfinding_handles_incorrect_target_room(load_mock_payload):
	payload = load_mock_payload
	payload['target_room'] = 'non_existent_sensor'
	response = client.post('/pathfinding/fastest-path', json=payload)
	assert response.status_code == 400
	assert response.json()['detail'] == "Target room 'non_existent_sensor' is not valid."


def test_pathfinding_handles_no_path(load_no_path_mock_payload):
	response = client.post('/pathfinding/fastest-path', json=load_no_path_mock_payload)
	assert response.status_code == 400
	assert response.json()['detail'] == 'No path found between the given rooms.'


def test_multiple_points_returns_correct_path(load_multiple_points_payload):
	response = client.post('/pathfinding/multiple-points', json=load_multiple_points_payload)

	assert response.status_code == 200
	data = response.json()
	assert 'fastest_path' in data
	assert 'distance' in data
	assert isinstance(data['distance'], (int, float))
	assert isinstance(data['fastest_path'], list)
	assert all(isinstance(sensor, dict) for sensor in data['fastest_path'])
	assert all(isinstance(point, dict) for point in data['fastest_path'])
	assert all(
		'id' in point and 'longitude' in point and 'latitude' in point
		for point in data['fastest_path']
	)


def test_multiple_points_handles_missing_data():
	response = client.post('/pathfinding/multiple-points', json={})
	assert response.status_code == 422

	expected_errors = [
		{'type': 'missing', 'loc': ['body', 'rooms'], 'msg': 'Field required', 'input': {}},
		{'type': 'missing', 'loc': ['body', 'sensors'], 'msg': 'Field required', 'input': {}},
		{'type': 'missing', 'loc': ['body', 'source_room'], 'msg': 'Field required', 'input': {}},
		{'type': 'missing', 'loc': ['body', 'target_rooms'], 'msg': 'Field required', 'input': {}},
	]
	assert response.json()['detail'] == expected_errors


def test_multiple_points_handles_incorrect_source_room(load_multiple_points_payload):
	payload = load_multiple_points_payload
	payload['source_room'] = 'non_existent_source_room'
	response = client.post('/pathfinding/multiple-points', json=payload)
	assert response.status_code == 400
	assert response.json()['detail'] == "Room 'non_existent_source_room' in the tour is not valid."


def test_multiple_points_handles_incorrect_target_room(load_multiple_points_payload):
	payload = load_multiple_points_payload
	payload['target_rooms'] = ['non_existent_target_room_1']
	response = client.post('/pathfinding/multiple-points', json=payload)
	data = response.json()
	assert response.status_code == 400
	assert data['detail'] == "Room 'non_existent_target_room_1' in the tour is not valid."


def test_multiple_points_handles_empty_target_rooms_list(
	load_multiple_points_payload,
):
	payload = load_multiple_points_payload
	payload['target_rooms'] = []
	response = client.post('/pathfinding/multiple-points', json=payload)
	data = response.json()
	assert response.status_code == 400
	assert (
		data['detail']
		== 'Target rooms list must contain at least one room different from the source room.'
	)


def test_multiple_points_handles_same_source_and_target(load_multiple_points_payload):
	payload = load_multiple_points_payload
	payload['target_rooms'] = [payload['source_room']]
	response = client.post('/pathfinding/multiple-points', json=payload)
	data = response.json()
	assert response.status_code == 400
	assert (
		data['detail']
		== 'Target rooms list must contain at least one room different from the source room.'
	)
