# Maze_Search.py

import numpy as np
from collections import deque
from Maze_class import Node, Node_Depth
from create_problem import MazeProblem


# Forward-Chaining to reach the goal
def forward_chaining(problem, goal):
    """Run forward chaining to determine if there is a path to the goal."""
    print("Initial Facts:", problem.facts)
    print("Goal:", goal)

    explored_cost = 0  # Total cost for each application of rules
    step = 1
    while goal not in problem.facts:
        print(f"\n--- Step {step} ---")
        problem.apply_rules()
        explored_cost += 1  # Count this step in the total exploration cost
        if goal in problem.facts:
            print(f"\nGoal {goal} reached after {step} steps.")
            print(f"Total explored cost: {explored_cost}")
            return True
        if not problem.apply_rules():
            print("No new inferences. Goal cannot be reached.")
            print(f"Total explored cost: {explored_cost}")
            return False
        step += 1

    print(f"\nGoal {goal} reached after {step - 1} steps.")
    print(f"Total explored cost: {explored_cost}")
    return True


# Depth-Limited Search
def depth_limited_search(problem, limit=50):
    explored_cost = 0  # Total explored cost

    def recursive_dls(node, problem, limit):
        nonlocal explored_cost
        explored_cost += 1  # Increment the cost for exploring this node

        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

    result = recursive_dls(Node_Depth(problem.initial), problem, limit)
    print(f"Total explored cost: {explored_cost}")
    return result


# Breadth-First Search (BFS)
def bfs(maze, start, end):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    rows, cols = len(maze), len(maze[0])

    queue = deque([start])
    visited = set([start])
    parent = {start: None}
    total_explored_cost = 0  # Initialize total cost for explored nodes

    while queue:
        current = queue.popleft()
        total_explored_cost += 1  # Increment the cost for exploring this node

        if current == end:
            break

        for direction in directions:
            new_row = current[0] + direction[0]
            new_col = current[1] + direction[1]
            new_node = (new_row, new_col)

            if 0 <= new_row < rows and 0 <= new_col < cols and maze[new_row][new_col] == 0 and new_node not in visited:
                queue.append(new_node)
                visited.add(new_node)
                parent[new_node] = current

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent.get(current)

    print(f"Total explored cost: {total_explored_cost}")
    return path[::-1], total_explored_cost


# A* Search
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


def search(maze, cost, start, end):
    start_node = Node(None, tuple(start))
    end_node = Node(None, tuple(end))

    yet_to_visit_list = [start_node]
    visited_list = []
    total_explored_cost = 0  # Initialize the total explored cost

    move_options = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    max_iterations = (len(maze) // 2) * 10
    outer_iterations = 0

    while len(yet_to_visit_list) > 0:
        outer_iterations += 1
        if outer_iterations > max_iterations:
            print("Too many iterations, exiting!")
            return None

        current_node = min(yet_to_visit_list, key=lambda node: node.f)
        yet_to_visit_list.remove(current_node)
        visited_list.append(current_node)

        total_explored_cost += current_node.g  # Add the cost of this step to the total

        if current_node == end_node:
            path_maze = return_path(current_node, maze)
            print(f"Total explored cost: {total_explored_cost}")
            return path_maze, total_explored_cost

        children = []
        for new_position in move_options:
            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])

            if (0 <= node_position[0] < len(maze) and
                    0 <= node_position[1] < len(maze[0]) and
                    maze[node_position[0]][node_position[1]] == 0):
                new_node = Node(current_node, node_position)
                children.append(new_node)

        for child in children:
            if child in visited_list:
                continue

            child.g = current_node.g + cost  # Increment the cost for each step
            child.h = ((child.position[0] - end_node.position[0]) ** 2 +
                       (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            yet_to_visit_list.append(child)

    return None
