# MazeProblem class
class MazeProblem:
    def __init__(self, maze, initial, goal):
        self.maze = maze
        self.initial = initial
        self.goal = goal
        self.rows = len(maze)
        self.cols = len(maze[0])

    def goal_test(self, state):
        return state == self.goal

    def successor(self, state):
        successors = []
        row, col = state
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.maze[new_row][new_col] == 0:
                successors.append((None, (new_row, new_col)))

        return successors

    def step_cost(self, current_state, action, next_state):
        return 1