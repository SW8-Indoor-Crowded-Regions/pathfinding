import networkx as nx
from db.database import Database

import matplotlib.pyplot as plt
from db.models.sensor import Sensor  # Your Sensor class
from db.models.room import Room      # Your Room class

# Initialize database connection
db = Database()

# --- Build the Graph ---
# Retrieve all sensors from the database.
sensors = list(Sensor.objects())

# Create an empty graph.
G = nx.Graph()

# Add each sensor as a node.
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

# --- Visualize the Graph ---
def visualize_graph(G):
    # Create a layout for the nodes.
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(8, 6))
    # Draw the nodes.
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=500)
    # Draw the edges.
    nx.draw_networkx_edges(G, pos, width=1.5, edge_color='gray')
    
    # Build custom labels: combine the names of the rooms for each sensor.
    labels = {}
    for sensor in sensors:
        # Assuming each room has a 'name' attribute.
        combined_name = "-".join([room.name for room in sensor.rooms])
        labels[sensor.id] = combined_name
    
    # Draw node labels using the custom labels.
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
    
    plt.title("Graph of Sensors Connected by Shared Rooms")
    plt.axis('off')
    plt.show()

# Call the function to display the graph.
visualize_graph(G)
