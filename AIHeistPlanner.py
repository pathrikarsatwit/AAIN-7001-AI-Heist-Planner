
from collections import deque


# TODO: Implement A*
class Heist_A_star:
    def __init__(self, start):
        self.start = start


# TODO: Implement BFS
class Heist_BFS:
    def __init__(self, start, treasure, exit, grid):
        self.start = start
        self.treasure = treasure
        self.exit = exit
        self.grid = grid

    def BFS(self):
        # State = (row, column, has_treasure)
        start_state = (self.start[0], self.start[1], False)

        frontier = deque([start_state])
        visited = {start_state}
        parent = {start_state: None}

        while frontier:
            node = frontier.popleft()

            if self.is_goal(node):
                path = []

                while node is not None:
                    path.append(node)
                    node = parent[node]

                return path[::-1]

            for child in self.expand(node):
                if child not in visited:
                    visited.add(child)
                    parent[child] = node
                    frontier.append(child)

        return None

    def expand(self, node):
        row, column, has_treasure = node
        children = []

        directions = [
            (-1, 0),  # Up
            (1, 0),   # Down
            (0, -1),  # Left
            (0, 1)    # Right
        ]

        for dr, dc in directions:
            new_row = row + dr
            new_column = column + dc

            if (0 <= new_row < len(self.grid)and 0 <= new_column < len(self.grid[0])):
                if self.grid[new_row][new_column] not in ["C", "X", "G"]:
                    # Check whether treasure has been collected
                    collected = has_treasure or (new_row, new_column) == self.treasure

                    children.append((new_row, new_column, collected))

        return children

    def is_goal(self, node):
        row, column, has_treasure = node
        return (row, column) == self.exit and has_treasure



class HeistPlanner:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.game_board = [[0 for _ in range(columns)] for _ in range(rows)]

        # Agent, treasure, and exit positions
        self.ai_agent_position = (0, 0)
        self.treasure_position = (7, 7)
        self.exit_position = (6, 0)

    # Print the grid
    def heist_grid(self, grid):
        for row in grid:
            print(*row, sep=" ")

    # Add AI agent
    def ai_agent(self):
        row, column = self.ai_agent_position
        self.game_board[row][column] = "A"
        return self.game_board

    # Add security cameras and danger zones
    def security_camera(self):
        self.ai_agent()

        security_camera_positions = [[4, 3], [5, 6]]

        for row, column in security_camera_positions:
            self.game_board[row][column] = "C"
            self.game_board[row][column - 1] = "X"
            self.game_board[row][column + 1] = "X"

        return self.game_board

    # Add security guards
    def security_guard(self):
        self.security_camera()

        security_guard_positions = [[7, 6], [2, 4]]

        for row, column in security_guard_positions:
            self.game_board[row][column] = "G"

        return self.game_board

    # Add treasure
    def treasure(self):
        self.security_guard()

        row, column = self.treasure_position
        self.game_board[row][column] = "T"

        return self.game_board

    # Add exit
    def exit(self):
        self.treasure()

        row, column = self.exit_position
        self.game_board[row][column] = "E"

        return self.game_board

    # Run BFS
    def run_solutions(self):
        grid = self.exit()

        print("\nOriginal Heist Grid:")
        self.heist_grid(grid)

        start = self.ai_agent_position
        treasure = self.treasure_position
        exit = self.exit_position

        ai_bfs = Heist_BFS(start, treasure, exit, grid)
        result = ai_bfs.BFS()

        if result:
            print("\nBFS Path:", result)
            print("Number of moves:", len(result) - 1)
        else:
            print("\nNo valid path found!")

        return result


# Run the program
heist = HeistPlanner(8, 8)
heist.run_solutions()
