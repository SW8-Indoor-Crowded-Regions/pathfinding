import matplotlib.pyplot as plt
import networkx as nx
import json

from app.classes.sensor import Sensor
from app.classes.sensor_graph import SensorGraph
from app.classes.room import Room

MOCK_DATA_PATH = 'app/test/mock_data/rooms_and_sensors.json'

def load_mock_payload():
    with open(MOCK_DATA_PATH, 'r') as f:
        return json.load(f)

def visualize_graph(G, path=None):
    # Create a layout for the nodes.
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(8, 6))
    # Draw the base graph: nodes and edges.
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=500)
    nx.draw_networkx_edges(G, pos, width=1.5, edge_color='gray')
    
    # Build custom labels: combine the names of the rooms for each sensor.
    labels = {}
    for node, data in G.nodes(data=True):
        sensor = data.get('sensor')
        if sensor and sensor.rooms:
            combined_name = "-".join(room.name for room in sensor.rooms)
        else:
            combined_name = str(node)  # fallback to the node id if sensor data is missing
        labels[node] = combined_name
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)
    
    # Prepare edge labels. For edges with multiple weights, display them as comma-separated values.
    edge_labels = {}
    for (u, v, data) in G.edges(data=True):
        label = f"{data.get('weight', 0):.2f}"
        edge_labels[(u, v)] = label
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)
    
    # If a fastest path is provided, highlight it.
    if path is not None:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='red')
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='orange', node_size=600)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[0]], node_color='green', node_size=700)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[-1]], node_color='purple', node_size=700)
    
    plt.title("Graph of Sensors with Fastest Path Highlighted")
    plt.axis('off')
    plt.show()
    
if __name__ == '__main__':
    payload = load_mock_payload()
    
    rooms = [Room.from_dict(room_data) for room_data in payload['rooms']]
    room_mapping = {room.id: room for room in rooms}
    
    sensors = []
    for sensor_data in payload['sensors']:
        sensor = Sensor.from_dict(sensor_data)
        sensor.attach_rooms(room_mapping)
        sensors.append(sensor)

    G = SensorGraph(sensors)
    G.build_graph()
    
    # Visualize the graph without highlighting a path.
    visualize_graph(G.graph)