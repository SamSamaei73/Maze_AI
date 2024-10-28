import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

def plot_maze():
    # Maze matrix (1 represents an obstacle, 0 represents a free path)
    maze = np.array([[0, 1, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0],
                     [0, 1, 0, 1, 0, 0],
                     [0, 1, 0, 0, 1, 0],
                     [0, 0, 0, 0, 1, 0]])

    fig, ax = plt.subplots()

    # Define a colormap: 0 -> lightblue, 1 -> red
    cmap = ListedColormap(['lightblue', 'red'])

    # Use imshow to display the maze (now with numerical values)
    cax = ax.imshow(maze, cmap=cmap, extent=[-0.5, 5.5, -0.5, 4.5], zorder=1)

    # Add grid lines
    ax.set_xticks(np.arange(-0.5, 6, 1), minor=False)
    ax.set_yticks(np.arange(-0.5, 5, 1), minor=False)
    ax.grid(which='both', color='black', linestyle='-', linewidth=2)

    # Set start and end points
    # ax.text(0, 0, 'Start', ha='center', va='center', fontsize=12, color='blue')
    # ax.text(5, 4, 'End', ha='center', va='center', fontsize=12, color='blue')

    # Label the positions of each node
    for i in range(5):
        for j in range(6):
            ax.text(j, i, f'({i},{j})', ha='center', va='center', fontsize=10)

    # Adjust plot limits and show the plot
    plt.xlim(0.5, 5.5)
    plt.ylim(0.5, 5.5)
    plt.title("Maze with Node Positions")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

plot_maze()
