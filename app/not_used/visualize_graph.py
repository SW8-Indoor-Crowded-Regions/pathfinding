import matplotlib.pyplot as plt
import networkx as nx

from app.classes.sensor import Sensor
from app.classes.sensor_graph import SensorGraph

import matplotlib.pyplot as plt
import networkx as nx

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
        if 'weights' in data:
            label = ", ".join(f"{w:.2f}" for w in data['weights'])
        else:
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
    # Create a graph with some nodes and edges.
    sensors = Sensor.create_sensors_from_schemas([], [])

    G = SensorGraph(sensors)
    G.load_graph('app/sensor_graph.pickle')
    
    # Visualize the graph without highlighting a path.
    visualize_graph(G.graph)