# Maze Algorithm

This repo contains the Maze algorithm that was created as a part of my assignment for an Algorithms graduate module. This script maze.py contains a class that creates a Cartesian-Coordinate maze represented as a Python dictionary tree, prints it into the console and implements two algorithms to find the route from point A to point B, provided that such route exists - locally greedy search based on the shortest L1 distance between the points at any iteration step and depth-first search.


The Maze class is initialized by creating and empty dictionary and a list of two zeros. The
dictionary is a graph-like representation of the maze. Every key of it keys represents an
open space in the maze, and its values are arrays of coordinates of connected open spaces
(nodes). The array describes the size of the maze for the purposes of printing it.

- **addCoordinate** - The add coordinate method updates the values of the two objects
initialized in the beginning. Firstly, whenever a coordinate is added that exceeds the
current size of the maze (as described by) the ’dim’ attribute) either horizontally or
vertically, the method updates dim, so it always corresponds with the largest values
of x and y. Secondly, if BlockType == 0 (i.e. the block is meant to be an open space), the
method uses a tuple of coordinates provided as a new key in the ’graph’ dictionary
and associates it with an empty array. Then, the function loops over all the possible
coordinates adjacent to the inserted coordinate and if they exist in the dictionary, it
adds the coordinates of the newly inserted coordinate to value array of each of the
adjacent coordinates. The converse also is applied, i.e. it also adds the coordinates of
all open spaces adjacent to the newly inserted coordinate to its array of values.
If, on the other hand, BlockType == 1 (i.e) its a wall, it pops the key-value pair
associated with the provided key from the dictionary. It also removes its coordinates
from value lists of the adjacent nodes of the graph. This way, if an existing open space
is changed into a wall, it will remove it from the open spaces list, as well as remove
any record of the connection from the adjacent nodes.
The graph representation of the Maze was chosen, as it allows representing the grid
structure of the Maze without storing unnecessary information about the walls - it
was the minimal possible representation of the Maze. Furthermore, it made the find-
Route algorithm more efficient than an array representation, which would possibly
require nested for-loops for x and y coordinates, potentially increasing the computa-
tional complexity of the algorithm. The graph representation also provided the most
intuitive representation of a series of connected corridors, making understanding of
the problem and looking for potential algorithm easier.

- **printMaze** - this method uses nested for loops, one representing the y coordinate,
the other the x coordinate. To determine the dimensions of the maze it uses the ’dim’
attribute updates by the addCoordinates method. This could be done simply by eval-
uating the highest value of the key tuple at index 0 and 1 for (x and y respectively)
in the graph attribute. However if the user added just one wall in a row or column
that is not yet within the boundaries of the maze previously, such wall would not be
printed, as it wouldn’t be recorded in the dictionary keys. For each ’y’ row it uses a
placeholder string variable and it loops over the x coordinates, adding * to the vari-
able if given combination of coordinates can be found in the graph dictionary keys and
space if not. At the end of each row iteration, it prints the string and resets it to empty.

- **findRoute** - this method finds the shortest between two points in the Maze. It’s a
greedy algorithm, picking the node with the closest Manhattan distance to the target
node at any given point in time. For any node it explores, it keeps track of the ’seen’
nodes, i.e. the nodes adjacent to the node that was set as current. If the algorithm
reaches a dead-end, it returns to a node on the ’seen’ list and picks the one with
shortest Manhattan distance to the destination, repeating the process. At the same
time, whenever a dead-end is reached, the list storing the path is erased up until the
unseen node the algorithm came back to. The choice of such approach is justified
by the fact that all the edges connecting the spaces in the Maze had equal weighting
(either difference of 1 in x coordinates or difference of 1 in y coordinates), therefore
finding the Manhattan distance was the best local approximation of the optimal route
to the target.


- **findRouteDepth** - this method finds the path between two points in the Maze. To do it, it uses the common depth-first search algorithm to find a point in the maze tree. It keeps track of the current path used by the algorithm, and as soon as the algorithm reaches destination, it returns the right path.
