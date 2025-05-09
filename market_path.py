```py
import streamlit as st
from queue import PriorityQueue
import folium # for maps
from streamlit_folium import st_folium
import osmnx as ox # for routing 
import networkx as nx
import os
import random
import math

def main():
    # st.set_page_config(page_title="Karachi Market Path Finder", layout="centered")

    st.markdown("""
        <style>
        .stApp {
            background-color: #f0f2f6;
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .stSelectbox > label {
            font-size: 1.1rem;
            font-weight: bold;
            color: #2c3e50;
        }
        .stButton>button {
            width: 100%;
            background-color: #3498db;
            color: white;
            padding: 0.75rem;
            border-radius: 8px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #2980b9;
        }
        .result-container {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin: 1.5rem 0;
        }
        .path-highlight {
            color: #e74c3c;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Market data with coordinates
    market_coords = {
        'Zainab Market': (24.8473, 67.0305),
        'Tariq Road': (24.8585, 67.0292),
        'Bahadurabad Market': (24.8557, 67.0512),
        'Hyderi Market': (24.9574, 67.0449),
        'Rabi Center': (24.9073, 67.0649),
        'Gul Plaza': (24.8493, 67.0255),
        'Tibbat Centre': (24.8612, 67.0518),
        'KDA Market': (24.9253, 67.0687),
        'Empress Market': (24.8600, 67.0207),
        'Bolton Market': (24.8603, 67.0138),
        'Jodia Bazaar': (24.8622, 67.0103),
        'Urdu Bazaar': (24.8610, 67.0294),
        'Light House': (24.8605, 67.0112)
    }

    # Create graph representation for A* algorithm
    def haversine_distance(coord1, coord2):
        # Haversine formula to calculate distance between two lat/lon coordinates in km
        R = 6371  # Earth radius in km
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        d_phi = math.radians(lat2 - lat1)
        d_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance_km = R * c
        return distance_km * 1000  # return in meters

    def generate_fully_connected_graph(coords):
        new_graph = {}
        for market1 in coords:
            new_graph[market1] = []
            for market2 in coords:
                if market1 != market2:
                    distance = haversine_distance(coords[market1], coords[market2])
                    cost = int(distance / 10)  # Scale down to simulate road travel cost
                    new_graph[market1].append((market2, cost))
        return new_graph

    graph = generate_fully_connected_graph(market_coords)

    def heuristic(node, goal):
        node_lat, node_lon = market_coords[node]
        goal_lat, goal_lon = market_coords[goal]

        lat_diff = abs(goal_lat - node_lat) * 111.32  #111.32 km is the approximate distance of 1 degree of latitude
        lon_diff = abs(goal_lon - node_lon) * 111.32 * abs(math.cos(math.radians((node_lat + goal_lat) / 2)))

        traffic_factor = random.uniform(1.0, 1.3)

        return (lat_diff + lon_diff) * traffic_factor

    def a_star(start, goal):
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        g_score = {market: float('inf') for market in market_coords}
        g_score[start] = 0

        f_score = {market: float('inf') for market in market_coords}
        f_score[start] = heuristic(start, goal)

        while not open_set.empty():
            current = open_set.get()[1]

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            for neighbor, cost in graph[current]:
                tentative_g_score = g_score[current] + cost

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set.queue]:
                        open_set.put((f_score[neighbor], neighbor))

        return None
    def filter_graph(G):
        """Filter out edges that violate constraints like access or unwanted road types"""
        G_filtered = G.copy()
        for u, v, k, data in G.edges(keys=True, data=True):
            if 'access' in data and data['access'] in ['private', 'no']:
                G_filtered.remove_edge(u, v, k)
            elif 'highway' in data and data['highway'] in ['service', 'pedestrian', 'footway', 'steps', 'track']:
                G_filtered.remove_edge(u, v, k)
        return G_filtered

# Implemented CSP to restrict algorithm to show path over buildings etc.
    class CSPPathFinder:
        def __init__(self, graph):
            self.graph = graph

        def solve(self, start_coords, end_coords):
            try:
                orig_node = ox.distance.nearest_nodes(self.graph, start_coords[1], start_coords[0])
                dest_node = ox.distance.nearest_nodes(self.graph, end_coords[1], end_coords[0])
                route = nx.shortest_path(self.graph, orig_node, dest_node, weight='length')
                return [[self.graph.nodes[node]['y'], self.graph.nodes[node]['x']] for node in route]
            except Exception as e:
                st.warning(f"Constraint Violation or Routing Failed: {e}")
                return None
            
    @st.cache_resource
    def load_karachi_graph():
        graph_path = "karachi_graph.graphml"

        if os.path.exists(graph_path):
            G = ox.load_graphml(graph_path)
        else:
            with st.spinner("Downloading Karachi map (only once)..."):
                G = ox.graph_from_place('Karachi, Pakistan', network_type='drive')
                ox.save_graphml(G, graph_path)
                st.success("Map saved to disk!")

        return G

    G = load_karachi_graph()
    G = filter_graph(G)  # Apply CSP filtering
    csp_router = CSPPathFinder(G)  # Create CSP based solver


    def get_actual_route(start_coords, end_coords):
        """Get actual road route using CSP constrained OSMnx graph"""
        return csp_router.solve(start_coords, end_coords)


    def plot_folium_map(path=None):
        lats = [coords[0] for coords in market_coords.values()]
        lons = [coords[1] for coords in market_coords.values()]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=13,
            tiles='OpenStreetMap',
            control_scale=True,
            width='100%',
            height='70vh'
        )

        for market, coords in market_coords.items():
            folium.Marker(
                location=coords,
                popup=market,
                icon=folium.Icon(color='red', icon='shopping-cart', prefix='fa')
            ).add_to(m)

        if path:
            all_route_coords = []

            for i in range(len(path) - 1):
                start = path[i]
                end = path[i + 1]
                start_coords = market_coords[start]
                end_coords = market_coords[end]

                route_coords = get_actual_route(start_coords, end_coords)

                if route_coords:
                    all_route_coords.extend(route_coords)
                else:
                    all_route_coords.extend([start_coords, end_coords])

            folium.PolyLine(
                all_route_coords,
                color='#3498db',
                weight=6,
                opacity=0.8,
                tooltip="Optimal Path",
                line_cap='round'
            ).add_to(m)

            folium.Marker(
                location=market_coords[path[0]],
                icon=folium.Icon(color='green', icon='play', prefix='fa'),
                tooltip=f"Start: {path[0]}"
            ).add_to(m)

            folium.Marker(
                location=market_coords[path[-1]],
                icon=folium.Icon(color='black', icon='flag-checkered', prefix='fa'),
                tooltip=f"Destination: {path[-1]}"
            ).add_to(m)

            for i, market in enumerate(path[1:-1], 1):
                folium.Marker(
                    location=market_coords[market],
                    icon=folium.Icon(color='orange', icon='dot-circle', prefix='fa'),
                    tooltip=f"Waypoint {i}: {market}"
                ).add_to(m)

        # Add layer control and fullscreen option
        folium.LayerControl().add_to(m)
        folium.plugins.Fullscreen().add_to(m)
        folium.plugins.MousePosition().add_to(m)

        return m

    st.title("Karachi Market Path Finder")

    col1, col2 = st.columns(2)
    with col1:
        start_market = st.selectbox("Select starting market", list(market_coords.keys()))
    with col2:
        goal_market = st.selectbox("Select destination market", list(market_coords.keys()))
        
    if st.button("Find Optimal Path", use_container_width=True):
        if start_market == goal_market:
            st.warning("Please select different start and destination markets")
        else:
            with st.spinner("Finding best path..."):
                path = a_star(start_market, goal_market)
                if path:
                    st.session_state["path"] = path
                else:
                    st.error("No path found between the selected markets")

    if "path" in st.session_state:
        path = st.session_state["path"]

        st.markdown(f"""
        <div class="result-container">
            <h3>Optimal Path from <span class="path-highlight">{start_market}</span> to <span class="path-highlight">{goal_market}</span></h3>
            <p>Total stops: {len(path)}</p>
            <ol>
                {"".join(f"<li>{market}</li>" for market in path)}
            </ol>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Route Map")
        st_folium(plot_folium_map(path), width=700, height=500)

    if 'path' not in locals():
        st.subheader("Karachi Markets Map")
        st_folium(plot_folium_map(), width=700, height=500)
        
if __name__ == "__main__":
    main()
      
```
