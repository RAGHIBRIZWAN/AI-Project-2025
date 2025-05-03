```py
import streamlit as st

# Custom CSS styling
css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

    .stApp {
        background-color: #f9fbfc;
        font-family: 'Roboto', sans-serif;
    }
    .title {
        color: #2c3e50;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .game-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.07);
        transition: transform 0.2s ease;
    }
    .game-card:hover {
        transform: translateY(-4px);
    }
    .game-title {
        color: #1abc9c;
        margin-bottom: 0.5rem;
        font-size: 1.5rem;
    }
    .game-description {
        color: #555;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1abc9c;
        color: white;
        padding: 0.75rem;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #16a085;
    }
    .back-button {
        margin-top: 2rem;
        background-color: #e74c3c !important;
    }
    .back-button:hover {
        background-color: #c0392b !important;
    }
    </style>
"""

def main_menu():
    """Display the main menu interface"""
    st.markdown("<h1 class='title'>Choose an Application</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='game-card'>
            <h2 class='game-title'>A* Escape Room</h2>
            <p class='game-description'>Navigate through a maze with constraint-based puzzles using the A* algorithm.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Open Escape Room", key="escape_room"):
            st.session_state['current_page'] = 'escape_room'
            st.rerun()

    with col2:
        st.markdown("""
        <div class='game-card'>
            <h2 class='game-title'>Karachi Market Path Finder</h2>
            <p class='game-description'>Find optimal paths between markets in Karachi using A* search.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Open Market Path Finder", key="market_finder"):
            st.session_state['current_page'] = 'market_finder'
            st.rerun()

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'main_menu'

# Page routing logic
if st.session_state['current_page'] == 'main_menu':
    st.set_page_config(
        page_title="App Selector",
        layout="centered",
        page_icon="🧭"
    )
    st.markdown(css, unsafe_allow_html=True)
    main_menu()
elif st.session_state['current_page'] == 'escape_room':
    try:
        from escape_room import main as escape_room_main
        st.markdown(css, unsafe_allow_html=True)
        if st.button("← Back to Main Menu", key="back_escape"):
            st.session_state['current_page'] = 'main_menu'
            st.rerun()
        escape_room_main()
    except Exception as e:
        st.error(f"Failed to load Escape Room: {str(e)}")
        st.session_state['current_page'] = 'main_menu'
        st.rerun()
elif st.session_state['current_page'] == 'market_finder':
    try:
        from market_path import main as market_finder_main
        st.markdown(css, unsafe_allow_html=True)
        if st.button("← Back to Main Menu", key="back_market"):
            st.session_state['current_page'] = 'main_menu'
            st.rerun()
        market_finder_main()
    except Exception as e:
        st.error(f"Failed to load Market Finder: {str(e)}")
        st.session_state['current_page'] = 'main_menu'
        st.rerun()
```
