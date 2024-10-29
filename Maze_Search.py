import numpy as np
from Maze_class import Node, Node_Depth
from create_problem import MazeProblem

# A* Search
def return_path(current_node, maze):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    path.reverse()  # Reverse the path to get from start to end

    # Initialize result maze with -1
    no_rows, no_columns = np.shape(maze)
    result = [[-1 for _ in range(no_columns)] for _ in range(no_rows)]

    # Fill in the path indices in the result maze
    for idx, position in enumerate(path):
        result[position[0]][position[1]] = idx  # Use idx for path index

    return result  # Return the maze with path marked

def search(maze, cost, start, end):
    start_node = Node(None, tuple(start))
    end_node = Node(None, tuple(end))

    yet_to_visit_list = [start_node]
    visited_list = []

    move_options = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    max_iterations = (len(maze) // 2) * 10
    outer_iterations = 0

    while len(yet_to_visit_list) > 0:
        outer_iterations += 1
        if outer_iterations > max_iterations:
            print("Too many iterations, exiting!")
            return None  # Return None if no path found

        current_node = min(yet_to_visit_list, key=lambda node: node.f)
        yet_to_visit_list.remove(current_node)
        visited_list.append(current_node)

        if current_node == end_node:
            path_maze = return_path(current_node, maze)
            total_cost = current_node.g  # Use g of the end node as total cost
            return path_maze, total_cost  # Return the maze with path and total cost

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

            child.g = current_node.g + cost  # Increment cost based on the current node's cost
            child.h = ((child.position[0] - end_node.position[0]) ** 2 +
                       (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            yet_to_visit_list.append(child)

    return None  # Return None if no path found

# Depth-Limited Search
# In your depth_limited_search function
def depth_limited_search(problem, limit=50):
    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node  # Return the node when the goal is reached
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result  # Return the goal node
            return 'cutoff' if cutoff_occurred else None

    return recursive_dls(Node_Depth(problem.initial), problem, limit)
