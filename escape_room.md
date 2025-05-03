```py
import random
from queue import PriorityQueue
import streamlit as st

# Inject custom CSS
css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

    .stApp {
        background-color: #f9fbfc;
        font-family: 'Roboto', sans-serif;
    }
    h1, h2, h3, .stSidebar h1 {
        color: #2c3e50;
        font-family: 'Roboto', sans-serif;
    }
    .stTable {
        font-size: 16px;
    }
    .css-1d391kg {  /* Expander */
        background-color: #ecf0f1 !important;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .stButton>button {
        background-color: #1abc9c;
        color: white;
        padding: 0.6rem 1.2rem;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #16a085;
    }
    .stSlider > div > div {
        color: #1abc9c;
    }
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

def main():
    SIZE = 8
    WALL = '#'
    OPEN = '.'
    START = 'S'
    GOAL = 'G'
    PUZZLE = 'P'
    WALL_PERCENT = 0.2
    PUZZLE_PERCENT = 0.1

    def generateGrid(wall_percent=WALL_PERCENT, puzzle_percent=PUZZLE_PERCENT):
        grid = [[OPEN for _ in range(SIZE)] for _ in range(SIZE)]
        startX, startY = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)
        grid[startX][startY] = START
        start = (startX, startY)

        while True:
            goalX, goalY = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)
            if (goalX, goalY) != (startX, startY):
                break
        grid[goalX][goalY] = GOAL
        goal = (goalX, goalY)

        wallCount = int(SIZE * SIZE * wall_percent)
        for _ in range(wallCount):
            x, y = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)
            if grid[x][y] == OPEN:
                grid[x][y] = WALL

        puzzleCount = int(SIZE * SIZE * puzzle_percent)
        for _ in range(puzzleCount):
            x, y = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)
            if grid[x][y] == OPEN:
                grid[x][y] = PUZZLE

        return grid, start, goal

    class Environment:
        def __init__(self, maze):
            self.maze = maze
            self.rows = len(maze)
            self.cols = len(maze[0])
            self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            self.puzzles_solved = []

        def is_valid(self, x, y, puzzles_solved):
            if not (0 <= x < self.rows and 0 <= y < self.cols):
                return False
            cell = self.maze[x][y]
            if cell == WALL:
                return False
            if cell == PUZZLE and (x, y) not in puzzles_solved:
                return False
            return True

        def heuristic(self, node, goal):
            return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

        def solve_lock_combination_puzzle(self, position):
            x, y = position
            digits = list(range(10))
            solution = {}

            def is_valid(d1, d2, d3):
                return d1 + d2 == 9 and d2 == 3 and d1 > d3

            for d1 in digits:
                for d2 in digits:
                    for d3 in digits:
                        if is_valid(d1, d2, d3):
                            solution = {"Digit 1": d1, "Digit 2": d2, "Digit 3": d3}
                            self.puzzles_solved.append((position, solution))
                            return True
            return False

        def astar(self, start, goal):
            pq = PriorityQueue()
            pq.put((0, [start]))
            visited = set()
            puzzles_solved = set()

            while not pq.empty():
                cost, path = pq.get()
                current = path[-1]

                if current == goal:
                    return path

                if current in visited:
                    continue
                visited.add(current)

                for dx, dy in self.directions:
                    nx, ny = current[0] + dx, current[1] + dy
                    if not (0 <= nx < self.rows and 0 <= ny < self.cols) or (nx, ny) in visited:
                        continue

                    cell = self.maze[nx][ny]
                    if cell == PUZZLE and (nx, ny) not in puzzles_solved:
                        if not self.solve_lock_combination_puzzle((nx, ny)):
                            continue
                        puzzles_solved.add((nx, ny))

                    if self.is_valid(nx, ny, puzzles_solved):
                        new_path = path + [(nx, ny)]
                        g_cost = len(new_path) - 1
                        h_cost = self.heuristic((nx, ny), goal)
                        f_cost = g_cost + h_cost
                        pq.put((f_cost, new_path))

            return None

    def draw_grid(grid, path):
        color_map = {
            START: 'S',
            GOAL: 'G',
            WALL: '##',
            PUZZLE: 'PZ',
            OPEN: '..'
        }

        grid_display = []
        for i in range(SIZE):
            row_display = []
            for j in range(SIZE):
                cell = grid[i][j]
                if (i, j) in path and cell not in (START, GOAL):
                    row_display.append('>>')
                else:
                    row_display.append(color_map.get(cell, '..'))
            grid_display.append(row_display)

        st.subheader("Maze View")
        st.table(grid_display)

    st.title("A* Escape Room")

    st.sidebar.header("Settings")
    wall_percent = st.sidebar.slider("Wall Percentage", 0.0, 1.0, WALL_PERCENT)
    puzzle_percent = st.sidebar.slider("Puzzle Percentage", 0.0, 1.0, PUZZLE_PERCENT)

    if st.sidebar.button("Generate New Room and Start A*"):
        grid, start, goal = generateGrid(wall_percent, puzzle_percent)
        env = Environment(grid)
        path = env.astar(start, goal)

        draw_grid(grid, path if path else [])

        st.subheader("Path Result")
        if path:
            st.success(f"Path found: {path}")
        else:
            st.error("Goal not reachable!")

        with st.expander("Solved CSP Puzzle Outputs"):
            if env.puzzles_solved:
                for position, solution in env.puzzles_solved:
                    st.markdown(
                        f"Puzzle at {position}: Combination - {solution['Digit 1']} {solution['Digit 2']} {solution['Digit 3']}"
                    )
            else:
                st.write("No puzzles encountered or solved.")

if __name__ == "__main__":
    main()

```
