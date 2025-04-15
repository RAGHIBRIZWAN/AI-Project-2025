import random
import streamlit as st
from queue import PriorityQueue
import matplotlib.pyplot as plt

st.set_page_config(page_title="Karachi Market Path Finder", layout="centered")

st.markdown("""
    <style>
    body {
        background-color: #f0f2f6;
    }

    .stApp {
        background-color: #f0f2f6;
        padding: 2rem;
        font-family: 'Segoe UI', sans-serif;
    }

    h1 {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }

    .stSelectbox > label {
        font-size: 1.1rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }

    .stSelectbox .css-1wa3eu0-placeholder {
        color: #999;
    }

    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 1rem;
    }

    .stButton>button {
        width: 60%;
        background-color: #3498db;
        color: white;
        padding: 0.85rem 1.5rem;
        border: none;
        border-radius: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }

    .stButton>button:hover {
        background-color: #2980b9;
    }

    .block-container {
        padding: 2rem 3rem;
    }

    .result-container {
        background-color: #ffffff;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
        margin-top: 1.5rem;
        color: #2c3e50;
        font-size: 1.05rem;
    }

    .path-highlight {
        color: #3498db;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Market coordinates
market_coords = {
    'Zainab Market': [24.8473, 67.0305],
    'Tariq Road': [24.8585, 67.0292],
    'Bahadurabad Market': [24.8557, 67.0512],
    'Hyderi Market': [24.9574, 67.0449],
    'Rabi Center': [24.9073, 67.0649],
    'Gul Plaza': [24.8493, 67.0255],
    'Tibbat Centre': [24.8612, 67.0518],
    'KDA Market': [24.9253, 67.0687],
    'Empress Market': [24.8600, 67.0207],
    'Bolton Market': [24.8603, 67.0138],
    'Jodia Bazaar': [24.8622, 67.0103],
    'Urdu Bazaar': [24.8610, 67.0294],
    'Light House': [24.8605, 67.0112]
}

# Graph representation
graph = {
    'Zainab Market': [('Tariq Road', 50), ('Bahadurabad Market', 60), ('Hyderi Market', 20), ('Rabi Center', 140), ('Gul Plaza', 25), ('Tibbat Centre', 70), ('KDA Market', 160), ('Empress Market', 60), ('Bolton Market', 80), ('Jodia Bazaar', 90), ('Urdu Bazaar', 60), ('Light House', 90)],
    'Tariq Road': [('Zainab Market', 50), ('Bahadurabad Market', 40), ('Hyderi Market', 30), ('Rabi Center', 100), ('Gul Plaza', 20), ('Tibbat Centre', 60), ('KDA Market', 150), ('Empress Market', 70), ('Bolton Market', 90), ('Jodia Bazaar', 80), ('Urdu Bazaar', 50), ('Light House', 70)],
    'Bahadurabad Market': [('Zainab Market', 60), ('Tariq Road', 40), ('Hyderi Market', 50), ('Rabi Center', 90), ('Gul Plaza', 30), ('Tibbat Centre', 50), ('KDA Market', 140), ('Empress Market', 80), ('Bolton Market', 70), ('Jodia Bazaar', 60), ('Urdu Bazaar', 40), ('Light House', 80)],
    'Hyderi Market': [('Zainab Market', 20), ('Tariq Road', 30), ('Bahadurabad Market', 50), ('Rabi Center', 110), ('Gul Plaza', 40), ('Tibbat Centre', 60), ('KDA Market', 130), ('Empress Market', 90), ('Bolton Market', 100), ('Jodia Bazaar', 80), ('Urdu Bazaar', 50), ('Light House', 70)],
    'Rabi Center': [('Zainab Market', 140), ('Tariq Road', 100), ('Bahadurabad Market', 90), ('Hyderi Market', 110), ('Gul Plaza', 60), ('Tibbat Centre', 50), ('KDA Market', 80), ('Empress Market', 70), ('Bolton Market', 90), ('Jodia Bazaar', 100), ('Urdu Bazaar', 60), ('Light House', 80)],
    'Gul Plaza': [('Zainab Market', 25), ('Tariq Road', 20), ('Bahadurabad Market', 30), ('Hyderi Market', 40), ('Rabi Center', 60), ('Tibbat Centre', 50), ('KDA Market', 70), ('Empress Market', 80), ('Bolton Market', 90), ('Jodia Bazaar', 60), ('Urdu Bazaar', 50), ('Light House', 70)],
    'Tibbat Centre': [('Zainab Market', 70 ), ('Tariq Road', 60), ('Bahadurabad Market', 50), ('Hyderi Market', 60), ('Rabi Center', 50), ('Gul Plaza', 50), ('KDA Market', 90), ('Empress Market', 80), ('Bolton Market', 70), ('Jodia Bazaar', 60), ('Urdu Bazaar', 50), ('Light House', 60)],
    'KDA Market': [('Zainab Market', 160), ('Tariq Road', 150), ('Bahadurabad Market', 140), ('Hyderi Market', 130), ('Rabi Center', 80), ('Gul Plaza', 70), ('Tibbat Centre', 90), ('Empress Market', 100), ('Bolton Market', 110), ('Jodia Bazaar', 120), ('Urdu Bazaar', 80), ('Light House', 90)],
    'Empress Market': [('Zainab Market', 60), ('Tariq Road', 70), ('Bahadurabad Market', 80), ('Hyderi Market', 90), ('Rabi Center', 70), ('Gul Plaza', 80), ('Tibbat Centre', 80), ('KDA Market', 100), ('Bolton Market', 90), ('Jodia Bazaar', 60), ('Urdu Bazaar', 50), ('Light House', 70)],
    'Bolton Market': [('Zainab Market', 80), ('Tariq Road', 90), ('Bahadurabad Market', 70), ('Hyderi Market', 100), ('Rabi Center', 90), ('Gul Plaza', 90), ('Tibbat Centre', 70), ('KDA Market', 110), ('Empress Market', 90), ('Jodia Bazaar', 80), ('Urdu Bazaar', 60), ('Light House', 70)],
    'Jodia Bazaar': [('Zainab Market', 90), ('Tariq Road', 80), ('Bahadurabad Market', 60), ('Hyderi Market', 80), ('Rabi Center', 100), ('Gul Plaza', 60), ('Tibbat Centre', 60), ('KDA Market', 120), ('Empress Market', 60), ('Bolton Market', 80), ('Urdu Bazaar', 50), ('Light House', 70)],
    'Urdu Bazaar': [('Zainab Market', 60), ('Tariq Road', 50), ('Bahadurabad Market', 40), ('Hyderi Market', 50), ('Rabi Center', 60), ('Gul Plaza', 50), ('Tibbat Centre', 50), ('KDA Market', 80), ('Empress Market', 50), ('Bolton Market', 60), ('Jodia Bazaar', 50), ('Light House', 60)],
    'Light House': [('Zainab Market', 90), ('Tariq Road', 70), ('Bahadurabad Market', 80), ('Hyderi Market', 70), ('Rabi Center', 80), ('Gul Plaza', 70), ('Tibbat Centre', 60), ('KDA Market', 90), ('Empress Market', 70), ('Bolton Market', 70), ('Jodia Bazaar', 70), ('Urdu Bazaar', 60)],
}

def heuristic(node, goal):
    if node not in market_coords or goal not in market_coords:
        return float('inf') 

    node_coords = market_coords[node]
    goal_coords = market_coords[goal]

    dx = abs(node_coords[0] - goal_coords[0])
    dy = abs(node_coords[1] - goal_coords[1])
    traffic_cost = random.randint(0, 100)

    return dx + dy + traffic_cost

def a_star(start, goal):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {market: float('inf') for market in market_coords}
    f_score = {market: float('inf') for market in market_coords}

    g_score[start] = 0
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

def plot_map(path=None):
    fig, ax = plt.subplots(figsize=(20,20))
    ax.set_facecolor('#ecf0f1') 
    label_positions = {}
    
    def is_overlapping(new_x, new_y, label_positions, threshold=0.002):
        for pos in label_positions.values():
            if abs(pos[0] - new_y) < threshold and abs(pos[1] - new_x) < threshold:
                return True
        return False

    for market, coords in market_coords.items():
        ax.scatter(coords[1], coords[0], color='#2c3e50', s=500, edgecolors='white', zorder=3)
        offset_x, offset_y = 0.0015, 0.0015  # Base offset

        while is_overlapping(coords[1] + offset_x, coords[0] + offset_y, label_positions):
            offset_x = random.uniform(0.001, 0.003) * random.choice([1, -1])
            offset_y = random.uniform(0.001, 0.003) * random.choice([1, -1])

        label_positions[market] = [coords[1] + offset_x, coords[0] + offset_y]

        ax.text(coords[1] + offset_x, coords[0] + offset_y, market, fontsize=9, ha='left', va='bottom')

    if path:
        for i in range(len(path) - 1):
            start_market = path[i]
            end_market = path[i + 1]
            start_coords = market_coords[start_market]
            end_coords = market_coords[end_market]
            ax.plot([start_coords[1], end_coords[1]], [start_coords[0], end_coords[0]], color='green', linewidth=2)

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Market Path Map')

    st.pyplot(fig)

# Streamlit UI setup
st.title("Pathfinding App with Map Visualization")

# User input for start and goal markets
start_market = st.selectbox("Select the start market", list(market_coords.keys()))
goal_market = st.selectbox("Select the destination market", list(market_coords.keys()))

# Button to calculate the path
if st.button("Find Path"):
    if start_market == goal_market:
        st.write("Start and goal markets are the same. Please select different markets.")
    else:
        path = a_star(start_market, goal_market)
        if path:
            # Display result
            st.markdown(f"""
                    <div class="result-container">
                        <p>🚩 <strong>Path from</strong> <span class="path-highlight">{start_market}</span> 
                        <strong>to</strong> <span class="path-highlight">{goal_market}</span>:</p>
                        <p style="margin-top:0.5rem;">🧭 {" → ".join(path)}</p>
                    </div>
                """, unsafe_allow_html=True)

            plot_map(path)  # Display map with the path
        else:
            st.write(f"No path found between {start_market} and {goal_market}.")
            
            st.markdown("""
    <hr style="margin-top:3rem;">
    <div style="text-align: center; color: #777;">
        Built with ❤️ using <a href="https://streamlit.io" target="_blank" style="color:#3498db;">Streamlit</a>
    </div>
""", unsafe_allow_html=True)
