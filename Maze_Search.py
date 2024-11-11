# Maze_Search.py

import numpy as np
from collections import deque
from Maze_class import Node, Node_Depth
from create_problem import MazeProblem


# Helper function to reconstruct the path in the maze grid
def return_path(current_node, maze):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    path.reverse()

    no_rows, no_columns = np.shape(maze)
    result = [[-1 for _ in range(no_columns)] for _ in range(no_rows)]

    for idx, position in enumerate(path):
        result[position[0]][position[1]] = idx

    return result


# A* Search Algorithm (no changes needed here)
def search(maze, cost, start, end):
    start_node = Node(None, tuple(start))
    end_node = Node(None, tuple(end))

    yet_to_visit_dict = {start_node.position: start_node}
    visited_dict = {}
    explored_cost = 0  # Track the total exploration cost

    move_options = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    max_iterations = (len(maze) // 2) * 10
    outer_iterations = 0

    while yet_to_visit_dict:
        outer_iterations += 1
        if outer_iterations > max_iterations:
            print("Too many iterations, exiting!")
            return None

        current_node = min(yet_to_visit_dict.values(), key=lambda node: node.f)
        current_position = current_node.position

        # Increment cost for visiting this node
        explored_cost += 1

        del yet_to_visit_dict[current_position]
        visited_dict[current_position] = current_node

        # Check if we have reached the goal
        if current_node == end_node:
            path_maze = return_path(current_node, maze)
            print(f"Total cost to reach the goal (including exploration): {explored_cost}")
            return path_maze, explored_cost  # Return the path and total exploration cost

        # Generate children
        children = []
        for new_position in move_options:
            node_position = (current_position[0] + new_position[0], current_position[1] + new_position[1])

            if (0 <= node_position[0] < len(maze) and
                    0 <= node_position[1] < len(maze[0]) and
                    maze[node_position[0]][node_position[1]] == 0):
                new_node = Node(current_node, node_position)
                children.append(new_node)

        # Loop through children
        for child in children:
            if child.position in visited_dict:
                continue  # Avoid revisiting nodes already fully explored

            # Calculate g, h, and f values for the child
            child.g = current_node.g + cost  # Increment cost for each step taken
            child.h = ((child.position[0] - end_node.position[0]) ** 2 +
                       (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # If the child is already in yet_to_visit_dict with a lower g cost, skip it
            if child.position in yet_to_visit_dict:
                existing_node = yet_to_visit_dict[child.position]
                if existing_node.g <= child.g:
                    continue

            # Add or update the child in yet_to_visit_dict
            yet_to_visit_dict[child.position] = child

    print("Goal not reachable")
    return None


# Updated Depth-Limited Search with Corrected Cost Calculation and Node Revisit Prevention
def depth_limited_search(problem, limit=50):
    explored_cost = 0  # Initialize explored cost to zero
    visited = set()  # Track visited nodes globally to prevent revisits

    def recursive_dls(node, problem, limit, visited_in_path):
        nonlocal explored_cost
        explored_cost += 1  # Increment for each node explored

        # Goal check
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                # Avoid revisiting nodes in the same path
                if child.state in visited or child.state in visited_in_path:
                    continue
                visited_in_path.add(child.state)  # Mark as visited in this path

                result = recursive_dls(child, problem, limit - 1, visited_in_path)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
                visited_in_path.remove(child.state)  # Remove from current path after exploration

            return 'cutoff' if cutoff_occurred else None

    # Start the recursive depth-limited search
    result = recursive_dls(Node_Depth(problem.initial), problem, limit, set())
    print(f"Total exploration cost (nodes visited): {explored_cost}")
    return result


# Breadth-First Search (BFS) with Corrected Cost Calculation and Node Revisit Prevention
def bfs(maze, start, end):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    rows, cols = len(maze), len(maze[0])

    queue = deque([(start, 0)])  # Queue now tracks both node and path cost
    visited = set([start])
    parent = {start: None}
    total_explored_cost = 0

    while queue:
        current, current_cost = queue.popleft()
        total_explored_cost += 1  # Increment for each node explored

        if current == end:
            break

        for direction in directions:
            new_row = current[0] + direction[0]
            new_col = current[1] + direction[1]
            new_node = (new_row, new_col)

            if (0 <= new_row < rows and 0 <= new_col < cols and
                    maze[new_row][new_col] == 0 and new_node not in visited):
                queue.append((new_node, current_cost + 1))
                visited.add(new_node)
                parent[new_node] = current

    # Reconstruct path from start to end
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent.get(current)

    print(f"Total cost to reach the goal (including exploration): {total_explored_cost}")
    return path[::-1], total_explored_cost
