# create_problem.py

class MazeProblem:
    def __init__(self, maze, initial, goal):
        self.maze = maze
        self.initial = initial
        self.goal = goal
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.facts = set()  # Stores facts about possible paths in the maze
        self.rules = [
            lambda x, y, z: ("path", x, y) in self.facts and ("path", y, z) in self.facts
        ]

    def goal_test(self, state):
        """Check if the state is the goal state."""
        return state == self.goal

    def step_cost(self, current_state, action, next_state):
        """Returns the cost of moving from current_state to next_state."""
        return 1  # Each move has a uniform cost of 1 in this maze

    def add_fact(self, fact):
        """Add a new fact about a path in the maze."""
        if fact not in self.facts:
            print(f"Adding fact: {fact}")
            self.facts.add(fact)

    def apply_rules(self):
        """Apply Forward-Chaining repeatedly to infer new paths."""
        while True:
            inferred_facts = set()
            for rule in self.rules:
                for fact1 in self.facts:
                    for fact2 in self.facts:
                        if fact1[1] == fact2[0]:  # Check if two facts can be chained
                            x, y, z = fact1[0], fact1[1], fact2[1]
                            if rule(x, y, z):
                                new_fact = ("path", x, z)
                                if new_fact not in self.facts and new_fact not in inferred_facts:
                                    inferred_facts.add(new_fact)
                                    print(f"Inferred new path: {new_fact}")

            if not inferred_facts:
                print("No more inferences possible.")
                break  # Exit the loop if no new inferences were made

            self.facts.update(inferred_facts)  # Add inferred facts

    def successor(self, state):
        """Generate successors for a given cell in the maze."""
        successors = []
        row, col = state
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.maze[new_row][new_col] == 0:
                successors.append((None, (new_row, new_col)))
                self.add_fact(("path", (row, col), (new_row, new_col)))  # Record initial paths

        return successors

    def initialize_facts(self):
        """Initialize facts based on open paths in the maze."""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze[row][col] == 0:
                    self.successor((row, col))  # Generates paths and adds facts
        print(f"Initial facts after setup: {self.facts}")
