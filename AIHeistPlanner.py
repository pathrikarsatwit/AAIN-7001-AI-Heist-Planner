from collections import deque
import time

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

# TODO: Implement A*
class Heist_A_star(HeistSearch):
    def __init__(self, start):
        self.start = start


# TODO: Implement BFS
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



class HeistPlanner:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

        # Agent, treasure, and exit positions
        self.ai_agent_position = (0, 0)
        self.treasure_position = (7, 7)
        self.exit_position = (6, 0)
        
        # Obstacles
        self.obstacles = [
            (1, 2), (1, 3),
            (2, 2), (3, 2),
            (5, 3), (5, 4)
        ]
        
        # Security camera positions
        self.camera_positions = [
            (4, 3), (5, 6)
        ]
        
        # Security guard positions
        self.guard_positions = [
            (7, 6), (2, 4)
        ]
       
    # Create the game board/grid 
    def create_game_board(self):
        grid = [
            ["." for _ in range(self.columns)] for _ in range(self.rows)
        ]
        
        # Add obstacles, cameras, and guards to the grid
        for row, column in self.obstacles:
            grid[row][column] = "#"
        
        for row, column in self.camera_positions:
            grid[row][column] = "C"
            
            for dc in [-1, 1]:
                new_column = column + dc
                
                if 0 <= new_column < self.columns:
                    if grid[row][new_column] == ".":
                        grid[row][new_column] = "X"
                        
        for row, column in self.guard_positions:
            grid[row][column] = "G"
            
            # Add treasure, exit, and AI agen to the grid
            tr, tc = self.treasure_position
            grid[tr][tc] = "T"
            
            er, ec = self.exit_position
            grid[er][ec] = "E"
            
            ar, ac = self.ai_agent_position
            grid[ar][ac] = "A"
            
            return grid
            

    # Print the grid
    def heist_grid(self, grid):
        print(" " + " ".join(str(c) for c in range(self.columns)))
        
        for r, row in enumerate(grid):
            print(r, " ".join(str(cell) for cell in row))
           
    # Display the BFS path on the grid 
    def show_path(self, path):
        grid = self.create_game_board()
        
        if path:
            for row, column, has_treasure in path[1:-1]:
                if (row, column) not in [
                    self.treasure_position,
                    self.exit_position
                ]:
                    grid[row][column] = "*"
                    
        print("\nMuseum with BFS Path (*):")
        self.heist_grid(grid)

    # Run BFS and display the results
    def run_solutions(self):
        grid = self.create_game_board()

        print("\nOriginal Heist Grid:")
        self.heist_grid(grid)

        bfs = Heist_BFS(
            start = self.ai_agent_position, 
            treasure = self.treasure_position, 
            exit = self.exit_position, 
            grid = grid
        )

        # Measure execution time for BFS
        start_time = time.perf_counter()
    
        bfs_path, explored = bfs.BFS()
    
        execution_time = time.perf_counter() - start_time
        
        print("\nBFS Results:")
        
        if bfs_path:
            print("Path:", bfs_path)
            print("Path length:", len(bfs_path) - 1)
            print("Nodes explored:", explored)
            print("Execution time: {execution_time:.6f} seconds")
            
            # Show the path on the grid
            self.show_path(bfs_path)
        else:
            print("No path found.")
            print("Nodes explored:", explored)
            print("Execution time: {execution_time:.6f} seconds")
            
        return bfs_path
    

# Run the program
if __name__ == "__main__":
    heist = HeistPlanner(8, 8)
    heist.run_solutions()