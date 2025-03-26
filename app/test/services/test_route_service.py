import json
import pytest
from app.controllers.route_service import create_fastest_path
from app.schemas.path import FastestPathRequest

GRAPH_PATH = 'app/test/mock_data/sensor_graph.pickle'
NO_PATH_GRAPH_PATH = 'app/test/mock_data/no_path_sensor_graph.pickle'
MOCK_DATA_PATH = 'app/test/mock_data/rooms_and_sensors.json'


@pytest.fixture
def load_mock_payload():
    with open(MOCK_DATA_PATH, 'r') as f:
        return json.load(f)


def test_source_not_in_graph(load_mock_payload):
    load_mock_payload['source_sensor'] = 'nonexistent_sensor'
    load_mock_payload['target_sensor'] = 'sensor2'
    request = FastestPathRequest.model_validate(load_mock_payload)

    with pytest.raises(ValueError) as e:
        create_fastest_path(request, GRAPH_PATH)
    assert 'Source sensor' in str(e.value)


def test_target_not_in_graph(load_mock_payload):
    load_mock_payload['source_sensor'] = '67d935b5d6d3ce76bef2c95a'
    load_mock_payload['target_sensor'] = 'nonexistent_sensor'
    request = FastestPathRequest.model_validate(load_mock_payload)

    with pytest.raises(ValueError) as e:
        create_fastest_path(request, GRAPH_PATH)
    assert 'Target sensor' in str(e.value)


def test_no_path_found_between_sensors(load_mock_payload):
    load_mock_payload['source_sensor'] = 'sensor1'
    load_mock_payload['target_sensor'] = '67d935b5d6d3ce76bef2c961'
    request = FastestPathRequest.model_validate(load_mock_payload)

    with pytest.raises(ValueError) as e:
        create_fastest_path(request, NO_PATH_GRAPH_PATH)
    assert 'No path found' in str(e.value)


def test_fastest_path_success(load_mock_payload):
    load_mock_payload['source_sensor'] = '67d935b5d6d3ce76bef2c962'
    load_mock_payload['target_sensor'] = '67d935b5d6d3ce76bef2c961'
    request = FastestPathRequest.model_validate(load_mock_payload)

    result = create_fastest_path(request, GRAPH_PATH)
    assert 'fastest_path' in result
    assert 'distance' in result
    assert isinstance(result['fastest_path'], list)
    assert isinstance(result['distance'], (int, float))
