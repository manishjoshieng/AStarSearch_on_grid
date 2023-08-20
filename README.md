# AStarSearch_on_grid
Path Finding with A Search Algorithm**

This repository contains an implementation of the A* Search algorithm for solving the path-finding problem in a grid-based environment. The goal is to find the optimal path from a fixed starting point to a fixed destination while navigating through obstacles with different costs.
Problem Description

In the path-finding problem, we have an 8x8 grid representing a maze-like environment. The grid contains various types of cells with different costs:

    Empty cells have a cost of +3.
    Bush plants are represented by cells with a cost of +4.
    Fire is represented by cells with a cost of +8.
    Walls are obstacles and cannot be traversed.

The task is to find the lowest-cost path from the given starting point (0,2) to the destination (6,4) while avoiding obstacles and minimizing the total cost.
Implementation Details

The A* Search algorithm is a widely used informed search algorithm that efficiently explores the search space by considering both the cost to reach a node (cost) and an estimated cost from the node to the goal (heuristic cost). The algorithm prioritizes nodes with lower final cost (f = g + h) to explore more promising paths first.

The main components of the implementation are:

    Grid Representation: The maze-like environment is represented as a grid. Each cell is associated with a specific cost based on the presence of obstacles, bushes, or fire.

    A* Search Algorithm: The AStarSearch function performs the A* Search algorithm to find the optimal path from the start node to the destination node. It utilizes a priority queue (heap) to efficiently explore nodes based on their f-cost.

    Heuristic Function: The heuristic function Position::distance is used to estimate the cost from any node to the goal node. In this implementation, the Manhattan distance heuristic is used, which is the sum of horizontal and vertical distances between two cells.

    Reconstruct Path: After finding the destination node, the recunstructPath function is used to reconstruct the lowest-cost path from the start node to the destination node.

How to Use

    Clone the repository to your local machine.

    Ensure you have Python (version >= 3.6) installed.

    Modify the location of the obstacles or add new obstacles variable in A_star_rabbit.py to represent your desired grid configuration.

    Run the A_star_rabbit.py script.

    The output will display the total cost of the path and the optimal path from the starting point to the destination.

Happy path finding!
