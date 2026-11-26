import heapq
import itertools
import random
import time
from collections import deque


class grid_layout:

    @classmethod
    def generate_layouts(cls, seed=None):
        rng = random.Random(seed)
        layouts = []

        for size in (10, 15, 20):
            for layout_number in range(1, 21):
                layout = cls()
                layout.rows = layout.columns = size
                layout.layout_id = f"{size}x{size}-{layout_number:02d}"
                layout.generate_game_elements(rng)
                layouts.append(layout)

        return layouts

    def create_game_board(self):

        # Create an empty board
        self.grid = [
            ["." for _ in range(self.columns)]
            for _ in range(self.rows)
        ]

        # Add obstacles
        for row, column in self.obstacles:
            self.grid[row][column] = "#"

        # Add cameras and their detection zones
        for row, column in self.camera_positions:
            self.grid[row][column] = "C"

            for dc in [-1, 1]:
                new_column = column + dc

                if (0 <= new_column < self.columns
                        and self.grid[row][new_column] == "."):
                    self.grid[row][new_column] = "X"

        # Add guards
        for row, column in self.guard_positions:
            self.grid[row][column] = "G"

        # Add treasure
        tr, tc = self.treasure_position
        self.grid[tr][tc] = "T"

        # Add exit
        er, ec = self.exit_position
        self.grid[er][ec] = "E"

        # Add AI agent
        ar, ac = self.ai_agent_position
        self.grid[ar][ac] = "A"

        return self.grid

    def generate_game_elements(self, rng):
        size = self.rows
        area = self.rows * self.columns
        obstacle_min = max(6, area // 24)
        obstacle_max = max(obstacle_min, area // 12)
        obstacle_count = rng.randint(obstacle_min, obstacle_max)
        camera_count = rng.randint(1, max(2, size // 5))
        guard_count = rng.randint(1, max(2, size // 5))

        # Keep the top row and rightmost column clear for a valid route.
        available_positions = [
            (row, column)
            for row in range(1, self.rows)
            for column in range(self.columns - 1)
        ]
        positions = rng.sample(
            available_positions,
            obstacle_count + camera_count + guard_count
        )

        self.obstacles = positions[:obstacle_count]
        self.camera_positions = positions[
            obstacle_count:obstacle_count + camera_count
        ]
        self.guard_positions = positions[obstacle_count + camera_count:]

        self.ai_agent_position = (0, 0)
        self.exit_position = (0, self.columns - 1)
        self.treasure_position = (self.rows - 1, self.columns - 1)

    # Print the grid
    def heist_grid(self, grid):
    # Print column headers
        print("    " + "".join(f"{c:3}" for c in range(self.columns)))
    # Print grid rows
        for r, row in enumerate(grid):
            print(f"{r:3} " + "".join(f"{cell:3}" for cell in row))

# Shared search logic for both BFS and A* search
class HeistSearch:
    def __init__(self, start, treasure, exit, grid):
        self.start = start
        self.treasure = treasure
        self.exit = exit
        self.grid = grid
        
        self.rows = len(grid)
        self.columns = len(grid[0])
        
    def is_valid(self, row, column):
        return (
            0 <= row < self.rows and
            0 <= column < self.columns and
            self.grid[row][column] not in ["C", "X", "G", "#"]
        )
        
    def expand(self, node):
        row, column, has_treasure = node
        children = []
        
        directions = [
            (-1, 0), # Up
            (1, 0), # Down
            (0, -1), # Left
            (0, 1) # Right
        ]
        
        for dr, dc in directions:
            new_row = row + dr
            new_column = column + dc
            
            if self.is_valid(new_row, new_column):
                collected = (has_treasure or (new_row, new_column) == self.treasure)
                children.append((new_row, new_column, collected))
        
        return children
    
    def is_goal(self, node):
        row, column, has_treasure = node
        return (row, column) == self.exit and has_treasure
    
    def reconstruct_path(self, parent, node):
        path = []
        
        while node is not None:
            path.append(node)
            node = parent[node]
            
        return path[::-1]

# A* Search Algorithm Implementation
class Heist_A_star(HeistSearch):

    def manhattan_distance(self, state):
        row, column, has_treasure = state

        if has_treasure:
            return (
                abs(row - self.exit[0]) +
                abs(column - self.exit[1])
            )

        distance_to_treasure = (
            abs(row - self.treasure[0]) +
            abs(column - self.treasure[1])
        )

        distance_to_exit = (
            abs(self.treasure[0] - self.exit[0]) +
            abs(self.treasure[1] - self.exit[1])
        )

        return distance_to_treasure + distance_to_exit

    def A_star(self):

        tie = itertools.count()

        start_state = (
            self.start[0],
            self.start[1],
            self.start == self.treasure
        )

        # Store: (f_cost, g_cost, tie_breaker, state)
        frontier = [
            (self.manhattan_distance(start_state),
             0, next(tie), start_state)
        ]

        best_g = {start_state: 0}
        parent = {start_state: None}

        explored = 0

        while frontier:

            _, g, _, node = heapq.heappop(frontier)

            if g > best_g.get(node, float("inf")):
                continue

            explored += 1

            if self.is_goal(node):
                path = self.reconstruct_path(parent, node)
                return path, explored

            for child in self.expand(node):

                child_g = g + 1

                if child_g < best_g.get(child, float("inf")):

                    best_g[child] = child_g
                    parent[child] = node

                    child_f = child_g + self.manhattan_distance(child)

                    heapq.heappush(
                        frontier,
                        (child_f, child_g, next(tie), child)
                    )

        return None, explored


# BFS Search Algorithm Implementation
class Heist_BFS(HeistSearch):
    def BFS(self):
        # State = (row, column, has_treasure)
        start_state = (self.start[0], self.start[1], self.start == self.treasure)

        frontier = deque([start_state])
        visited = {start_state}
        parent = {start_state: None}
        
        explored = 0

        while frontier:
            node = frontier.popleft()
            explored += 1

            if self.is_goal(node):
                path = self.reconstruct_path(parent, node)
                return path, explored

            for child in self.expand(node):
                if child not in visited:
                    visited.add(child)
                    parent[child] = node
                    frontier.append(child)

        return None, explored


# Manages the heist planning including the grid, game elements, and running the search algorithms
class HeistPlanner:

    def __init__(self, grid_layout):

        self.grid_layout = grid_layout

        # Store positions in HeistPlanner
        self.ai_agent_position = self.grid_layout.ai_agent_position
        self.treasure_position = self.grid_layout.treasure_position
        self.exit_position = self.grid_layout.exit_position

    # Display BFS path on the grid
    def show_path(self, path, original_grid, algorithm):
        grid = [row[:] for row in original_grid]
        if path:
            for row, column, has_treasure in path[1:-1]:
                if (row, column) not in [
                    self.treasure_position,
                    self.exit_position]:
                    grid[row][column] = "*"
        print(f"\nMuseum with {algorithm} Path (*):")
        self.grid_layout.heist_grid(grid)

    # Run A* and BFS
    def run_solutions(self):
        grid = self.grid_layout.create_game_board()
        print("\nOriginal Heist Grid:")

        self.grid_layout.heist_grid(grid)

        bfs = Heist_BFS(
            start=self.ai_agent_position,
            treasure=self.treasure_position,
            exit=self.exit_position,
            grid=grid
        )

        a_star = Heist_A_star(
            start=self.ai_agent_position,
            treasure=self.treasure_position,
            exit=self.exit_position,
            grid=grid
        )

        # Measure execution time for A*
        start_time = time.perf_counter()
        a_star_path, a_star_explored = a_star.A_star()
        execution_time_a_star = time.perf_counter() - start_time

        # Measure execution time for BFS
        start_time = time.perf_counter()
        bfs_path, bfs_explored = bfs.BFS()
        execution_time_bfs = time.perf_counter() - start_time

        # Display the results for A*
        print("\nA* Results:")
        if a_star_path:
            print("Path: ", [(row, column) for row, column, _ in a_star_path])
            print("Path length: ", len(a_star_path) - 1)
            print("Nodes explored: ", a_star_explored)
            print(f"Execution time: {execution_time_a_star:.6f} seconds")
            
            # Display A* path on grid
            self.show_path(a_star_path, grid, "A*")
        else:
            print("No path found.")
            print("Nodes explored: ", a_star_explored)
            print(f"Execution time: {execution_time_a_star:.6f} seconds")

        # Display the results for BFS 
        print("\nBFS Results:")

        if bfs_path:
            print("Path: ", [(row, column) for row, column, _ in bfs_path])
            print("Path length: ", len(bfs_path) - 1)
            print("Nodes explored: ", bfs_explored)
            print(f"Execution time: {execution_time_bfs:.6f} seconds")
            
            # Show the BFS path on the grid
            self.show_path(bfs_path, grid, "BFS")
        else:
            print("No path found.")
            print("Nodes explored: ", bfs_explored)
            print(f"Execution time: {execution_time_bfs:.6f} seconds")

        return bfs_path
    

# Run the program
if __name__ == "__main__":
    layouts = grid_layout.generate_layouts()
    selected_layout = random.choice(layouts)
    heist = HeistPlanner(selected_layout)
    heist.run_solutions()