import random
from queue import PriorityQueue
import streamlit as st

# Set wide layout
st.set_page_config(layout="wide")

# Grid size
SIZE = 8

# Cell types
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
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        self.puzzles_solved = []  # To track solved puzzles

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
        print(f"🔒 Solving Lock Combination Puzzle at ({x}, {y})!")
        digits = [0, 1, 2, 3, 4, 5,  6, 7, 8, 9]
        solution = {}

        def is_valid(digit1, digit2, digit3):
            return digit1 + digit2 == 9 and digit2 == 3 and digit1 > digit3

        for digit1 in digits:
            for digit2 in digits:
                for digit3 in digits:
                    if is_valid(digit1, digit2, digit3):
                        solution = {"Digit 1": digit1, "Digit 2": digit2, "Digit 3": digit3}
                        self.puzzles_solved.append((position, solution))
                        print(f"✅ Puzzle at ({x}, {y}) solved!")
                        return True  

        print(f"❌ Could not solve the puzzle at ({x}, {y}).")
        return False 

    def astar(self, start, goal):
        pq = PriorityQueue()
        pq.put((0, [start]))  # (f_cost, path)
        visited = set()
        puzzles_solved = set()

        while not pq.empty():
            cost, path = pq.get()
            current = path[-1]

            if current == goal:
                return path  # Found the goal!

            if current in visited:
                continue
            visited.add(current)

            for dx, dy in self.directions:
                nx, ny = current[0] + dx, current[1] + dy

                if not (0 <= nx < self.rows and 0 <= ny < self.cols):
                    continue

                if (nx, ny) in visited:
                    continue

                cell = self.maze[nx][ny]

                if cell == PUZZLE and (nx, ny) not in puzzles_solved:
                    if not self.solve_lock_combination_puzzle((nx, ny)):
                        continue  # Could not solve, skip this direction
                    puzzles_solved.add((nx, ny))  # Mark it solved

                if self.is_valid(nx, ny, puzzles_solved):
                    new_path = path + [(nx, ny)]
                    g_cost = len(new_path) - 1
                    h_cost = self.heuristic((nx, ny), goal)
                    f_cost = g_cost + h_cost
                    pq.put((f_cost, new_path))

        return None  # No path found

def draw_grid(grid, path):
    st.write("### 🗺️ Escape Room Map")
    color_map = {
        START: '🟢',
        GOAL: '🔴',
        WALL: '⬛',
        PUZZLE: '🟨',
        OPEN: '⬜'
    }

    # Create a grid display with larger blocks
    grid_display = []
    for i in range(SIZE):
        row_display = []
        for j in range(SIZE):
            cell = grid[i][j]
            if (i, j) in path and cell not in (START, GOAL):
                row_display.append('🔷')
            else:
                row_display.append(color_map.get(cell, '⬜⬜⬜'))  # Larger normal block
        grid_display.append(row_display)

    # Display the grid as a table for better spacing
    st.table(grid_display)

st.title("🧠 A* Escape Room with Puzzle Integration")

st.sidebar.header("Settings")
wall_percent = st.sidebar.slider("Wall Percentage", 0.0, 1.0, WALL_PERCENT)
puzzle_percent = st.sidebar.slider("Puzzle Percentage", 0.0, 1.0, PUZZLE_PERCENT)

if st.sidebar.button("🔁 Generate New Room and Start A*"):
    grid, start, goal = generateGrid(wall_percent, puzzle_percent)
    env = Environment(grid)
    path = env.astar(start, goal)

    draw_grid(grid, path if path else [])

    st.write("### Path Result")
    if path:
        st.success(f"✅ Path found: {path}")
    else:
        st.error("❌ Goal not reachable!")
    
    if env.puzzles_solved:
        with st.expander("📜 Solved CSP Puzzle Outputs"):
            for position, solution in env.puzzles_solved:
                st.markdown(f"Puzzle at {position}: Combination - {solution['Digit 1']} {solution['Digit 2']} {solution['Digit 3']}")
    else:
        with st.expander("📜 Solved CSP Puzzle Outputs"):
            st.write("No puzzles encountered or solved.")
