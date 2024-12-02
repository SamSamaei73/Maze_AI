from collections import deque
from Maze_class import Node_Depth

def depth_limited_search(problem, limit=50):
    """
    Depth-Limited Search (DLS) with correct cost calculation.
    Counts all unique nodes explored during the search, including wrong steps.
    """
    explored_nodes = set()  # Set to store all unique nodes visited

    def recursive_dls(node, problem, limit):
        nonlocal explored_nodes

        # Count the current node if it's not already in explored_nodes
        if node.state not in explored_nodes:
            explored_nodes.add(node.state)

        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                if child.state not in explored_nodes:  # Avoid revisiting nodes in the recursion
                    result = recursive_dls(child, problem, limit - 1)
                    if result == 'cutoff':
                        cutoff_occurred = True
                    elif result is not None:
                        return result
            return 'cutoff' if cutoff_occurred else None

    start_node = Node_Depth(problem.initial)
    result = recursive_dls(start_node, problem, limit)
    return result, len(explored_nodes)  # Return the result and total explored cost


def bfs(maze, start, end):
    """
    Breadth-First Search (BFS) with correct cost calculation.
    Counts all unique nodes explored during the search, including wrong steps.
    """
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    rows, cols = len(maze), len(maze[0])

    queue = deque([start])
    visited = set([start])  # Set to store all unique nodes visited
    parent = {start: None}

    while queue:
        current = queue.popleft()

        if current == end:
            break

        for direction in directions:
            new_row, new_col = current[0] + direction[0], current[1] + direction[1]
            new_node = (new_row, new_col)

            if (0 <= new_row < rows and 0 <= new_col < cols and
                    maze[new_row][new_col] == 0 and new_node not in visited):
                queue.append(new_node)
                visited.add(new_node)  # Mark as visited
                parent[new_node] = current

    # Reconstruct the path from start to end
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent.get(current)

    return path[::-1], len(visited)  # Return path and total explored cost
