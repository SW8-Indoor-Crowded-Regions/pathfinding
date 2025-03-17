from fastapi import FastAPI
from routes.routing import router
from config import CORS_SETTINGS
from fastapi.middleware.cors import CORSMiddleware
from classes.data_fetcher import DataFetcher
from classes.sensor_graph import SensorGraph


app = FastAPI(title="Routing")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_SETTINGS["allow_origins"],
    allow_credentials=CORS_SETTINGS["allow_credentials"],
    allow_methods=CORS_SETTINGS["allow_methods"],
    allow_headers=CORS_SETTINGS["allow_headers"],
)

def main():
    # Initialize the data fetcher and retrieve sensors and rooms.
    fetcher = DataFetcher()
    sensors = fetcher.get_sensors()
    rooms = fetcher.get_rooms()

    # Create a mapping from room id to Room object.
    room_mapping = {room.id: room for room in rooms}

    # Attach full Room objects to each Sensor.
    for sensor in sensors:
        sensor.attach_rooms(room_mapping)

    # Build the sensor graph.
    graph_obj = SensorGraph(sensors)
    graph_obj.build_graph()

    # Define source and target sensor IDs for the example.
    if len(sensors) > 1:
        # Use specific indices if available; otherwise, default to the first and last sensors.
        try:
            source_sensor_id = sensors[15].id
            target_sensor_id = sensors[40].id
        except IndexError:
            source_sensor_id = sensors[0].id
            target_sensor_id = sensors[-1].id

        path, total_weight = graph_obj.find_fastest_path(source_sensor_id, target_sensor_id)

        if path:
            # For each transition, determine the common room names.
            room_path = []
            for u, v in zip(path, path[1:]):
                sensor_u = graph_obj.graph.nodes[u]['sensor']
                sensor_v = graph_obj.graph.nodes[v]['sensor']
                rooms_u = {room.name for room in sensor_u.rooms}
                rooms_v = {room.name for room in sensor_v.rooms}
                common_rooms = rooms_u.intersection(rooms_v)
                room_path.append(", ".join(common_rooms) if common_rooms else "No common room")

            print("Fastest path (room names along each transition):")
            print(room_path)
            print("Total effective weight (sum of crowd factors):", total_weight)
        else:
            print("No path found between the selected sensors.")
    else:
        print("Not enough sensors to determine a path.")


# ROUTING ROUTER
app.include_router(router)

if __name__ == "__main__":
    main()

# In production use Gunicorn to run Uvicorn with workers
# Below is an example with -w 4 meaning 4 workers processes assigned
#
# pip install gunicorn
# gunicorn -k uvicorn.workers.UvicornWorker -w 4 app.main:app
