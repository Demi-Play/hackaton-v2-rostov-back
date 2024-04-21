import folium
import osmnx as ox
import requests

def build_optimal_route(start_coords, end_coords):
    # Create a folium map centered on the start location
    route_map = folium.Map(location=start_coords, zoom_start=13)

    # Add start and end markers
    start_marker = folium.Marker(location=start_coords, popup='Start', icon=folium.Icon(color='green'))
    end_marker = folium.Marker(location=end_coords, popup='End', icon=folium.Icon(color='red'))
    start_marker.add_to(route_map)
    end_marker.add_to(route_map)

    # Find the optimal route
    G = ox.graph_from_point(start_coords, dist=2000, network_type='drive')
    start_node = ox.nearest_nodes(G, start_coords[1], start_coords[0])
    end_node = ox.nearest_nodes(G, end_coords[1], end_coords[0])
    route = ox.shortest_path(G, start_node, end_node, weight='length')

    # Add the route to the map
    route_coords = [[G.nodes[route[i]]['y'], G.nodes[route[i]]['x']] for i in range(len(route))]
    folium.PolyLine(route_coords, color='blue', weight=5, opacity=0.7).add_to(route_map)

    # Display the map
    return route_map

if __name__ == "__main__":
    start_coords = (55.792596, 37.774863)
    end_coords = (55.799863, 37.787912)
    optimal_route_map = build_optimal_route(start_coords, end_coords)
    optimal_route_map.save("optimal_route.html")
