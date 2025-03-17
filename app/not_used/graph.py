import requests
import networkx as nx
from types import SimpleNamespace

def dict_to_obj(data):
    """
    Recursively convert dictionaries (or lists of dictionaries)
    into objects for attribute-style access.
    """
    if isinstance(data, dict):
        return SimpleNamespace(**{k: dict_to_obj(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [dict_to_obj(item) for item in data]
    else:
        return data

def fetch_data(url: str):
    """
    Fetch JSON data from the given URL and return the parsed JSON.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_sensors() -> list:
    """
    Retrieve the sensors data from the sensors endpoint.
    If the JSON contains a key "sensors", extract it; otherwise, assume
    the response is the sensor list directly.
    """
    sensors_json = fetch_data("http://localhost:8002/sensors/")
    if isinstance(sensors_json, dict) and "sensors" in sensors_json:
        sensors_list = sensors_json["sensors"]
    else:
        sensors_list = sensors_json
    return [dict_to_obj(sensor) for sensor in sensors_list]

def get_rooms() -> list:
    """
    Retrieve the rooms data from the rooms endpoint.
    If the JSON contains a key "rooms", extract it; otherwise, assume
    the response is the room list directly.
    """
    rooms_json = fetch_data("http://localhost:8002/rooms/")
    if isinstance(rooms_json, dict) and "rooms" in rooms_json:
        rooms_list = rooms_json["rooms"]
    else:
        rooms_list = rooms_json
    return [dict_to_obj(room) for room in rooms_list]

def build_graph(sensors: list) -> nx.Graph:
    """
    Build a graph where each sensor is a node and edges are created between
    sensors that share a room. The edge weight is based on the room's crowd_factor.
    """
    G = nx.Graph()

    # Add each sensor as a node with its sensor object attached.
    for sensor in sensors:
        G.add_node(sensor.id, sensor=sensor)

    # Group sensors by the rooms they belong to.
    room_to_sensors = {}
    for sensor in sensors:
        for room in sensor.rooms:
            room_id = str(room.id)
            if room_id not in room_to_sensors:
                room_to_sensors[room_id] = {'room': room, 'sensors': []}
            room_to_sensors[room_id]['sensors'].append(sensor)

    # Create edges between sensors that share the same room.
    for room_info in room_to_sensors.values():
        room = room_info['room']
        sensors_in_room = room_info['sensors']
        weight = room.crowd_factor  # Use room's crowd_factor as edge weight.
        for i in range(len(sensors_in_room)):
            for j in range(i + 1, len(sensors_in_room)):
                sensor1 = sensors_in_room[i]
                sensor2 = sensors_in_room[j]
                if G.has_edge(sensor1.id, sensor2.id):
                    if 'weights' in G[sensor1.id][sensor2.id]:
                        G[sensor1.id][sensor2.id]['weights'].append(weight)
                    else:
                        existing_weight = G[sensor1.id][sensor2.id].pop('weight')
                        G[sensor1.id][sensor2.id]['weights'] = [existing_weight, weight]
                else:
                    G.add_edge(sensor1.id, sensor2.id, weight=weight)

    return G

def find_fastest_path(G: nx.Graph, source, target):
    """
    Finds the fastest path between source and target sensor nodes using Dijkstra's algorithm.
    For edges with multiple weights, the sum of the weights is used.
    Returns the path as a list of sensor IDs and the total effective weight.
    """
    weight_func = lambda u, v, d: sum(d['weights']) if 'weights' in d else d['weight']
    try:
        path = nx.dijkstra_path(G, source, target, weight=weight_func)
        distance = nx.dijkstra_path_length(G, source, target, weight=weight_func)
        return path, distance
    except nx.NetworkXNoPath:
        return None, None

def main():
    # Fetch sensors and rooms from their respective endpoints.
    sensors = get_sensors()
    rooms = get_rooms()

    # Build a mapping from room id to room object for quick lookup.
    room_mapping = {room.id: room for room in rooms}

    # Convert each sensor's room IDs into full room objects.
    for sensor in sensors:
        sensor.rooms = [room_mapping[room_id] for room_id in sensor.rooms if room_id in room_mapping]

    # Build the graph based on sensors and their rooms.
    G = build_graph(sensors)

    # Define source and target sensors for the example (first and last sensor in the list).
    if len(sensors) > 1:
        source_sensor = sensors[15].id
        target_sensor = sensors[40].id

        fastest_path, fastest_distance = find_fastest_path(G, source_sensor, target_sensor)

        if fastest_path:
            # Build a list of room names for each transition along the fastest path.
            room_path = []
            for u, v in zip(fastest_path, fastest_path[1:]):
                sensor_u = G.nodes[u]['sensor']
                sensor_v = G.nodes[v]['sensor']
                # Extract the room names from both sensors.
                rooms_u = {room.name for room in sensor_u.rooms}
                rooms_v = {room.name for room in sensor_v.rooms}
                common_rooms = rooms_u.intersection(rooms_v)
                room_path.append(", ".join(common_rooms) if common_rooms else "No common room")

            print("Fastest path (room names along each transition):")
            print(room_path)
            print("Total effective weight (sum of crowd factors):", fastest_distance)
        else:
            print("No fastest path found between the chosen sensors.")
    else:
        print("Not enough sensors to define a source and target.")

if __name__ == '__main__':
    main()
