class MazeProblem:
    def __init__(self, maze, initial, goal):
        self.maze = maze
        self.initial = initial
        self.goal = goal
        self.rows = len(maze)
        self.cols = len(maze[0])

    def goal_test(self, state):
        """Check if the state is the goal state."""
        return state == self.goal

    def step_cost(self, current_state, action, next_state):
        """Returns the cost of moving from current_state to next_state."""
        return 1  # Each move has a uniform cost of 1 in this maze

    def successor(self, state):
        """Generate successors for a given cell in the maze."""
        successors = []
        row, col = state
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.maze[new_row][new_col] == 0:
                successors.append((None, (new_row, new_col)))

        return successors
