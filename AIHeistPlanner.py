# Todo: AI Heist Planner Agent - solved using A* and BFS

#Todo: Main Grid - Grid 8 x 8
from collections import deque

#Todo: Implement A* 

class Heist_A_star:
    def __init__(self, start):
        self.start = start


#Todo: Implement BFS
class Heist_BFS:
    def __init__(self):
        pass
    def BFS(self):
        frontier = deque([self.start])
        while frontier:
            node = frontier.popleft()
            for child in self.expand(node):
                if self.is_goal(child):
                    return child
                frontier.append(child)
                
    def expand(self):
        pass
    
    def is_goal(self):
        pass
    
class HeistPlanner:
    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows
        self.game_board = [[0 for _ in range(columns)] for _ in range(rows)]

    # Create a 8 x8 grid - print the grid
    def heist_grid (self, grid) -> None:
        for row in grid:
            print(*row, sep=" ")
        

    #add AI agent -  A for AI Agent
    def ai_agent (self) -> list:
        ai_agent_position = [0,0]
        self.game_board[ai_agent_position[0]][ai_agent_position[1]] = "A"
        return self.game_board
        
    #add security cameras - print C for security camera, mark x in spots on left and right of the camera
    def security_camera (self) -> list:
        self.game_board = self.ai_agent()
        security_camera_position = [[4,3], [5,6]]
        for i in range(len(security_camera_position)):
            security_camera_row = security_camera_position[i][0]
            security_camera_column = security_camera_position[i][1]
            self.game_board[security_camera_row][security_camera_column] = "C"
            left_column = security_camera_column - 1
            right_column = security_camera_column + 1
            self.game_board[security_camera_row][left_column] = "X"
            self.game_board[security_camera_row][right_column] = "X"
        return self.game_board

    #add security guard - print G for security guard
    def security_guard (self) -> list:
        self.game_board = self.security_camera()
        security_guard_positions = [[7,6], [2,4]]
        for i in range(len(security_guard_positions)):
            self.game_board[security_guard_positions[i][0]][security_guard_positions[i][1]] = "G"

        return self.game_board


    #add treasure - print T for treasure
    def treasure (self) -> list:
        self.game_board = self.security_guard()
        treasure_position = [7,7]
        self.game_board[treasure_position[0]][treasure_position[1]] = "T"
        print(self.game_board)
        return self.game_board
    
    #add exit - print E for exit
    def exit (self) -> list:
        self.game_board = self.treasure()
        exit_position = [6,0]
        self.game_board[exit_position[0]][exit_position[1]] = "E"
        return self.game_board

    #call a* and bfs
    def run_solutions(self) -> None:
        grid = self.exit()
        self.heist_grid(grid)
        
        
heist = HeistPlanner(8,8)
print(heist.run_solutions())

        



