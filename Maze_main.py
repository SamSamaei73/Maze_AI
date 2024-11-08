from Maze_Search import search

def run_maze_search(start, end):
    maze = [[0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0]]

    cost = 1
    path = search(maze, cost, start, end)

    return path
