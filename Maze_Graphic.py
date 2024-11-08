# Maze_Graphic.py

import tkinter as tk
from tkinter import messagebox
from Maze_main import run_maze_search
from Maze_Search import depth_limited_search, bfs, forward_chaining
from create_problem import MazeProblem

def find_path():
    try:
        start_x = int(start_x_entry.get())
        start_y = int(start_y_entry.get())
        end_x = int(end_x_entry.get())
        end_y = int(end_y_entry.get())
        limit = int(depth_limit_entry.get()) if search_algo.get() == "Depth-Limited Search" else None
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid integers for start and end coordinates.")
        return

    start = (start_x, start_y)
    end = (end_x, end_y)

    maze = [[0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0]]

    if maze[start[0]][start[1]] == 1:
        messagebox.showerror("Invalid Start Position", "The start position is in a blocked cell. Please choose an open cell.")
        return
    if maze[end[0]][end[1]] == 1:
        messagebox.showerror("Invalid End Position", "The end position is in a blocked cell. Please choose an open cell.")
        return

    problem = MazeProblem(maze, start, end)
    problem.initialize_facts()
    goal_fact = ("path", start, end)

    if search_algo.get() == "A* Search":
        path_maze, total_cost = run_maze_search(start, end)
        if path_maze:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END,
                               '\n'.join([''.join(["{:<3}".format(item) for item in row]) for row in path_maze]))
            cost_label.config(text=f"Total cost to reach the goal: {total_cost}")
        else:
            messagebox.showinfo("No Path", "No valid path found!")
    elif search_algo.get() == "Depth-Limited Search":
        path_node = depth_limited_search(problem, limit=limit)
        if path_node != 'cutoff':
            path = path_node.path()
            total_cost = path_node.path_cost
            result_text.delete(1.0, tk.END)
            path_display = ['({},{})'.format(pos[0], pos[1]) for pos in path]
            result_text.insert(tk.END, '\n'.join(path_display))
            cost_label.config(text=f"Total explored cost: {total_cost}")
        else:
            messagebox.showinfo("No Path", "No valid path found!")
    elif search_algo.get() == "Breadth-First Search":
        path, total_cost = bfs(maze, start, end)
        if path:
            result_text.delete(1.0, tk.END)
            path_display = ['({},{})'.format(pos[0], pos[1]) for pos in path]
            result_text.insert(tk.END, '\n'.join(path_display))
            cost_label.config(text=f"Total explored cost to reach the goal: {total_cost}")
        else:
            messagebox.showinfo("No Path", "No valid path found!")
    elif search_algo.get() == "Forward-Chaining":
        result = forward_chaining(problem, goal_fact)
        if result:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Goal reached using Forward-Chaining.")
            cost_label.config(text="Goal state reached successfully.")
        else:
            messagebox.showinfo("No Path", "No valid path found!")

root = tk.Tk()
root.title("Maze Search")

tk.Label(root, text="Start Position (x, y):").grid(row=0, column=0, padx=10, pady=5)
start_x_entry = tk.Entry(root, width=5)
start_y_entry = tk.Entry(root, width=5)
start_x_entry.grid(row=0, column=1)
start_y_entry.grid(row=0, column=2)

tk.Label(root, text="End Position (x, y):").grid(row=1, column=0, padx=10, pady=5)
end_x_entry = tk.Entry(root, width=5)
end_y_entry = tk.Entry(root, width=5)
end_x_entry.grid(row=1, column=1)
end_y_entry.grid(row=1, column=2)

tk.Label(root, text="Depth Limit (only for Depth-Limited Search):").grid(row=2, column=0, padx=10, pady=5)
depth_limit_entry = tk.Entry(root, width=5)
depth_limit_entry.grid(row=2, column=1)

search_algo = tk.StringVar(value="A* Search")
tk.Label(root, text="Select Search Algorithm:").grid(row=3, column=0, padx=10, pady=5)
tk.Radiobutton(root, text="A* Search", variable=search_algo, value="A* Search").grid(row=3, column=1)
tk.Radiobutton(root, text="Depth-Limited Search", variable=search_algo, value="Depth-Limited Search").grid(row=3, column=2)
tk.Radiobutton(root, text="Breadth-First Search", variable=search_algo, value="Breadth-First Search").grid(row=3, column=3)
tk.Radiobutton(root, text="Forward-Chaining", variable=search_algo, value="Forward-Chaining").grid(row=3, column=4)

search_button = tk.Button(root, text="Find Path", command=find_path)
search_button.grid(row=4, column=0, columnspan=5, pady=10)

result_text = tk.Text(root, height=10, width=40)
result_text.grid(row=5, column=0, columnspan=5, padx=10, pady=10)

cost_label = tk.Label(root, text="", font=("Arial", 12))
cost_label.grid(row=6, column=0, columnspan=5, pady=5)

root.mainloop()
# /////////test/////