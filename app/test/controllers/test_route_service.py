import json
import pytest
from app.controllers.route_service import create_fastest_path
from app.schemas.path import FastestPathRequest

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


def test_source_not_in_graph(load_mock_payload):
	load_mock_payload['source_room'] = 'nonexistent_sensor'
	load_mock_payload['target_room'] = '67d935b5d6d3ce76bef2c961'
	request = FastestPathRequest.model_validate(load_mock_payload)

	with pytest.raises(ValueError) as e:
		create_fastest_path(request)
	assert 'Source room' in str(e.value)


def test_target_not_in_graph(load_mock_payload):
	load_mock_payload['source_room'] = '67d935b5d6d3ce76bef2c962'
	load_mock_payload['target_room'] = 'nonexistent_room'
	request = FastestPathRequest.model_validate(load_mock_payload)

	with pytest.raises(ValueError) as e:
		create_fastest_path(request)
	assert 'Target room' in str(e.value)


def test_no_path_found_between_sensors(load_no_path_mock_payload):
	request = FastestPathRequest.model_validate(load_no_path_mock_payload)

	with pytest.raises(ValueError) as e:
		create_fastest_path(request)
	assert 'No path found' in str(e.value)


def test_fastest_path_success(load_mock_payload):
	request = FastestPathRequest.model_validate(load_mock_payload)

	result = create_fastest_path(request)
	assert 'fastest_path' in result
	assert 'distance' in result
	assert isinstance(result['fastest_path'], list)
	assert isinstance(result['distance'], (int, float))
	assert result['fastest_path'] == [
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
	assert pytest.approx(result['distance']) == 0.09
