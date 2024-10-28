# Node class for A* Search
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0  # Cost from start node
        self.h = 0  # Heuristic cost
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

# Node_Depth class for Depth-Limited Search
class Node_Depth:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def expand(self, problem):
        """Return a list of child nodes generated from this node."""
        return [Node_Depth(next_state, self, action, problem.step_cost(self.state, action, next_state))
                for action, next_state in problem.successor(self.state)]

    def path(self):
        """Return the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node.state)
            node = node.parent
        return list(reversed(path_back))