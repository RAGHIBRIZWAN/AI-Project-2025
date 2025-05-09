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
      
```
