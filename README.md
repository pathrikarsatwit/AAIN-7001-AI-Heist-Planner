# AAIN-7001-AI-Heist-Planner

## Project Overview
The AI Heist Planner is a Python-based project that simulates a museum heist using AI Search Algorithms. An AI-controlled thief must navigate through a museum, collect a treasure, and find the exit without bumping into any obstacles or security elements (security cameras and guards.)

The project uses two search algorithms: A* Search and Breadth-First Search (BFS), to find paths through the museum. Both performance will be compared based on their path length, number of nodes explored, and execution time. Users will be able to test different layouts of the museum by changing the positions of obstacles, security cameras, guards, the tresure, and the exit in the code.

## Project Objectives
- Develop a simulation of a 2D grid based museum.
- Implement A* Search and BFS algorithms for path finding.
- Find a safe path that allows the agent/thief to collec the treasure and exit without getting caught.
- Avoid obstacles, security cameras, camera detection zones, and guards.
- Compare the performance of A* and BFS using different measurements.

## Technologies Used
- Python: Main programming language
- Collection (deque): Used to implement the BFS queue
- Heapq: Used to manage the A* priority queue
- It tools (itertools):
- Time - used to measure algorithm execution time

## Museum Grid
The museum is represented as a 2D grid. Each cell represents a location that the agent/thief can move through or an element that may affect its path.
| Symbol |             Description            |
|--------|------------------------------------|
|    A   |           AI agent/thief           |
|    T   |               Treasure             |
|    E   |             Museum exit            |
|    #   |               Obstacle             |
|    C   |           Security camera          |
|    X   |         Camera dection zone        |
|    G   |           Security guard           |
|    .   |           Available space          |
|    *   | Path found by the search algorithm |

## Search Algorithms
### A* Search
A* explores the museum grid by prioritizing the states that appear closest to the goal. It uses a priority queue to keep track of which states to explore next, considering both the cost of the path taken so far and the estimated distance remaining to the goal. By using the manhattan distance heuristic, A* can guide the search toward the treasure and then the exit more efficiently. Because every move has the same cost and the heuristic is admissible, A* can find an optimal path when a valid path exists.

### Breadth-First Search (BFS)
BFS explores the museum grid level by level, checking neighboring locations before moving farther away. It uses a queue to keep track of the states that need to be explored. Because every move has the same cost, BFS can find a shortest path to the goal when a valid path exists.

## Evaluation Metrics
The two search algorithms will be compared using the following measurements:
- Path length: Numbers of movements required to collect the treasure and exit the museum.
- Nodes explored: Number of states explored by each algorithm.
- Execution time: The time required for each algorithm to complete its search of path.
- Success rate: Percentage of museum layouts where an algorithm finds a valid path.

Both search algorithms will be tested using the same museum layouts to keep the consistency and fairness when comparing the two.