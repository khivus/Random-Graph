# Random Graph Generator and BFS Traversal

This program generates a random graph using tkinter in Python and performs a breadth-first search (BFS) traversal on the graph. The graph consists of nodes represented as circles and links represented as lines connecting the nodes.

## Prerequisites
- Python 3.x
- Tkinter library
- win32api library
- numericUpDown module (provided)

## Installation
1. Clone the repository or download the program files.
2. Install the required libraries if not already installed:
   ```
   pip install tkinter
   pip install pywin32
   ```
   
## Usage
To run the program, execute the following command:
```
python main.py
```

The program window will open, and you can interact with the graph using the buttons provided.

### Adding Nodes
- Click the "add" button to add nodes to the graph.
- Use the numeric up-down control to specify the number of nodes to add.
- Nodes will be randomly placed within the canvas area and will have unique labels.

### Clearing the Graph
- Click the "clear" button to remove all nodes and links from the graph.
- This will reset the graph to its initial state.

### Breadth-First Search Traversal
- Click the "Breadth-first search" button to perform a BFS traversal on the graph.
- The traversal will start from the first node (labeled 1).
- The traversal order will be displayed in the output label.

### Printing the Adjacency Matrix
- Click the "print adjacency matrix" button to print the adjacency matrix of the graph.
- The adjacency matrix represents the connections between nodes.
- 1 indicates a connection, and 0 indicates no connection.

### Animating the BFS Traversal
- Click the "animate" button to animate the BFS traversal on the graph.
- The traversal will start from the first node (labeled 1).
- The nodes visited during the traversal will be highlighted in green, and the links traversed will become thicker and black.
- The traversal order will be displayed in the output label.

Note: The animation may be blocked if the "add" button is clicked while the animation is in progress.

## Customization
You can customize the following parameters in the code:

- `TIME_DELAY`: The delay (in seconds) between each step of the animation.
- `NUMBER_OF_NODES`: The maximum number of nodes that can be added to the graph.
- `NODE_RADIUS`: The radius of the nodes in pixels.
- The probability and number of links created between nodes can be adjusted in the `add_node` function.

Feel free to modify these parameters according to your requirements.

## License
This program is licensed under the [MIT License](LICENSE).
