import networkx as nx
from db.database import Database

import matplotlib.pyplot as plt
from db.models.sensor import Sensor  # Your Sensor class
from db.models.room import Room      # Your Room class


'''

To not make a tight coupling between DB and this
ALL communication with DB is now through
sensorsim/dataprocessing repo

refer to endpoint file.

'''




# Initialize database connection
db = Database()

# --- Build the Graph ---
# Retrieve all sensors from the database.
sensors = list(Sensor.objects())

# Create an empty graph.
G = nx.Graph()

# Add each sensor as a node with the sensor object attached.
for sensor in sensors:
    G.add_node(sensor.id, sensor=sensor)

# Group sensors by each room they belong to.
room_to_sensors = {}
for sensor in sensors:
    # Each sensor is associated with a list of rooms.
    for room in sensor.rooms:
        room_id = str(room.id)  # Use string form of room id for consistency.
        if room_id not in room_to_sensors:
            room_to_sensors[room_id] = {'room': room, 'sensors': []}
        room_to_sensors[room_id]['sensors'].append(sensor)

# Create edges between sensors that share the same room.
for room_info in room_to_sensors.values():
    room = room_info['room']
    sensors_in_room = room_info['sensors']
    weight = room.crowd_factor  # Use room's crowd factor as edge weight.
    for i in range(len(sensors_in_room)):
        for j in range(i + 1, len(sensors_in_room)):
            sensor1 = sensors_in_room[i]
            sensor2 = sensors_in_room[j]
            if G.has_edge(sensor1.id, sensor2.id):
                # If edge exists from a previous shared room, add the new weight.
                if 'weights' in G[sensor1.id][sensor2.id]:
                    G[sensor1.id][sensor2.id]['weights'].append(weight)
                else:
                    # Convert existing single weight to a list and add the new one.
                    existing_weight = G[sensor1.id][sensor2.id].pop('weight')
                    G[sensor1.id][sensor2.id]['weights'] = [existing_weight, weight]
            else:
                # Create a new edge with the room's crowd factor as the weight.
                G.add_edge(sensor1.id, sensor2.id, weight=weight)

# --- Visualization Function with Fastest Path Highlight ---
def visualize_graph(G, path=None):
    # Create a layout for the nodes.
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(8, 6))
    # Draw the base graph: nodes and edges.
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=500)
    nx.draw_networkx_edges(G, pos, width=1.5, edge_color='gray')
    
    # Build custom labels: combine the names of the rooms for each sensor.
    labels = {}
    for sensor in sensors:
        combined_name = "-".join([room.name for room in sensor.rooms])
        labels[sensor.id] = combined_name
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)
    
    # Prepare edge labels. For edges with multiple weights, display them as comma-separated values.
    edge_labels = {}
    for (u, v, data) in G.edges(data=True):
        if 'weights' in data:
            label = ", ".join(f"{w:.2f}" for w in data['weights'])
        else:
            label = f"{data['weight']:.2f}"
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

# --- Dijkstra's Algorithm Implementation ---
def find_fastest_path(G, source, target):
    """
    Finds the fastest path from source to target using Dijkstra's algorithm.
    Returns the path as a list of sensor nodes and the total effective weight.
    """
    # Define a custom weight function:
    # If an edge has multiple weights, use the sum of weights; otherwise, use the single weight.
    weight_func = lambda u, v, d: sum(d['weights']) if 'weights' in d else d['weight']
    
    try:
        path = nx.dijkstra_path(G, source, target, weight=weight_func)
        distance = nx.dijkstra_path_length(G, source, target, weight=weight_func)
        return path, distance
    except nx.NetworkXNoPath:
        print(f"No path exists between {source} and {target}.")
        return None, None

# --- Example Usage ---
# Define source and target sensors.
source_sensor = sensors[15].id   # Example: using the sensor at index 15 as source.
target_sensor = sensors[40].id   # Example: using the sensor at index 40 as target.

fastest_path, fastest_distance = find_fastest_path(G, source_sensor, target_sensor)

if fastest_path is not None:
    # Build a list of room names for the fastest path by checking the common room(s)
    # between each pair of consecutive sensors.
    room_path = []
    for u, v in zip(fastest_path, fastest_path[1:]):
        sensor_u = G.nodes[u]['sensor']
        sensor_v = G.nodes[v]['sensor']
        # Gather room names from both sensors.
        rooms_u = {room.name for room in sensor_u.rooms}
        rooms_v = {room.name for room in sensor_v.rooms}
        # Find the common room(s).
        common_rooms = rooms_u.intersection(rooms_v)
        if common_rooms:
            # If multiple common rooms exist, join them with a comma.
            room_path.append(", ".join(common_rooms))
        else:
            room_path.append("No common room")
    
    print("Fastest path (room names along each transition):")
    print(room_path)
    print("Total effective weight (sum of crowd factors):", fastest_distance)
else:
    print("No fastest path found.")

# Visualize the graph with the fastest path highlighted.
visualize_graph(G, path=fastest_path)
