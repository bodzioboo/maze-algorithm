


class Maze:
    def __init__(self):

        self.graph = dict()
        self.dim = [0,0]

            
    def addCoordinate(self,x,y,blocType):
        """
        Add information about a coordinate on the maze grid
        x is the x coordinate
        y is the y coordinate
        blockType should be 0 (for an open space) of 1 (for a wall)
        
        DESCRIPTION:
        The add coordinate method populates a dictionary self.graph, which is graph like
        reresentation of the maze. Each key is a vertex, which is a tuple of coordinates (x,y)
        each value for a given key is an array of vertices (x,y) connected to that vertex in the maze.
        """
        
        #update the dimensions:
        #useful for creating boundary rows that are entirely rows and 
        #thus not captured by the graph representation, which would left them unprinted
        if x > self.dim[0]:
            self.dim[0] = x
        
        if y > self.dim[1]:
            self.dim[1] = y
            
        
        if blocType == 0: #if inserting a space
            self.graph[(x,y)] = [] #create an empty arary at the coordinates
            for key in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)): #for all the possible adjacent coordinates:
                if key in self.graph.keys(): #if coordinate already in graph
                    #update the existsing adjecent vertices with the coordinate of new vertex
                    self.graph[key].append((x,y))
                    #update the new vertex with coordinates of all adjecent vertices:
                    self.graph[(x,y)].append(key)
                    
        if blocType == 1: #if inserting a wall
            self.graph.pop((x,y),None) #remove the vertex from graph
            for key in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)): #for adjecent vertices
                #remove record of adjecency:
                if key in self.graph.keys():
                    self.graph[key] = [elem for elem in self.graph[key] if elem != (x,y)]
    
    
    def printMaze(self):
        """
        Print out an ascii representation of the maze.
        A * indicates a wall and a empty space indicates an open space in the maze
        
        DESCRIPTION:
        the printMaze method prints the representation of the maze.This is done by nested loops, one for values of y from 0 to maximum included in the maze,
        the other similar, but for values of x within the yth row. For each row, if a coordinate is in the
        graph representation of the maze, it prints an star, if not, a space.
        
        """
        for i in range(self.dim[1]+1): #for each row y
            temp_string = '' #reset value of temp_string to empty
            for j in range(self.dim[0]+1): #for each x in row y
                if (j,i) in self.graph.keys(): #if point is a vertex
                    temp_string += ' ' #add space to represent open space
                else:
                    temp_string += '*' #add star to represent wall 
            print(temp_string) #print
                
    
    def findRoute(self,x1,y1,x2,y2):
        """
		This method should find a route, traversing open spaces, from the coordinates (x1,y1) to (x2,y2)
		It should return the list of traversed coordinates followed along this route as a list of tuples (x,y),
		in the order in which the coordinates must be followed
		If no route is found, return an empty list
        
        DESCRIPTION: a greedy algorithm, always choosing the vertex closest to the destination as the next
        one to be explored. In case of hitting a dead end, returns to all the vertices that were seen on 
        the way but not explored.
		"""
        #verify given points aren't walls:
        if (x1,y1) not in self.graph.keys() or (x2,y2) not in self.graph.keys():
            print('One of the points provided is a wall.')
            return None
        current_vertex = (x1,y1)
        path = [] #storing the path
        visited_vertices = set() #storing the visited vertices
        distances_from_target = dict() #keeping the Manhattan distances from target vertexs
        while current_vertex != (x2,y2):
            visited_vertices.add(current_vertex) #add the current vertex to visited vertexs
            distances_from_target.pop(current_vertex,None)
            path.append(current_vertex) #add the current vertex to the path to target
            for vertex in self.graph[current_vertex]: #for all the vertices neighbouring with current
                if vertex not in visited_vertices: #if vertex wasn't visited yet
                    distances_from_target[vertex] = abs(x2-vertex[0])+abs(y2-vertex[1]) #calculate the manhattan distance from destination for each of the neighbour vertices
            #choice set for the next vertex: all unexplored vertices with calculated distances to the target which are connected with the current vertex
            choices = {k:v for k,v in distances_from_target.items() if k in self.graph[current_vertex]}
            if choices: #if there are any connections from current vertex, 
                current_vertex = min(choices, key = choices.get) #pick the one with lowest distance
            else: #if there is no way to go further
                #try to go back to a unexplored vertex with shortest distance from target and search again.
                try: #erase the path record up until the newly selected vertex
                    new_vertex = min(distances_from_target, key = distances_from_target.get)
                    distance = abs(new_vertex[0]-current_vertex[0])+abs(new_vertex[1]-current_vertex[1]) #distance between the new choice adn the last vertex to erase from path
                    path = path[:len(path)-distance+1]
                    current_vertex = new_vertex
                except :#if that's not possible, no route can be found
                    print('No route found')
                    return None
        path.append((x2,y2))
        return path
    

                    

    def findRouteDepth(self,x1,y1,x2,y2):
        """
        This is an alternative implementation of the findRoute method based
        on the Depth First Search algorithm. 
        It creates a list called stack, used for storing seen vertices waiting to be processed,
        a set called visited used to store already processed vertexs and a dictionary paths, 
        used for storing all the paths explored by the Depth First Search.
        """
        if (x1,y1) not in self.graph.keys() or (x2,y2) not in self.graph.keys():
            print('One of the points provided is a wall.')
        stack = [(x1,y1)]
        visited = set(stack)
        paths = dict()
        i = 0
        while stack != []:
            v = stack.pop() #pop the vertex from stack of seen vertces
            if not paths: #for the first iteration: if the dictionary is empty
                paths[i] = [v]
            elif v in self.graph[paths[i][-1]]: #add vertex v to the path if the previous vertex in the path was adjacent
                paths[i].append(v)
            else: #else, create a new path by keeping all the elements of the previous path until the element adjecent to the vertex
                last = [elem for elem in paths[i] if elem in self.graph[v]][0]
                i += 1
                paths[i] = paths[i-1][:paths[i-1].index(last)+1]
                paths[i].append(v)
            #whenever destination is reached, return the current path
            if v == (x2,y2):
                return paths[i]
            #DFS: put the seen vertices on stack and mark them as visited
            for vertex in self.graph[v]:
                if vertex not in visited:
                    stack.append(vertex)
                    visited.add(vertex)
        print('Path not found!')
        return None
    

def mazeTest():
    """
    This sets the open space coordinates for the example
    maze in the assignment.
    The remainder of coordinates within the max bounds of these specified coordinates
    are assumed to be walls
    """
    myMaze = Maze()
    myMaze.addCoordinate(1,0,0)
    myMaze.addCoordinate(1,1,0)
    myMaze.addCoordinate(7,1,0)
    myMaze.addCoordinate(1,2,0)
    myMaze.addCoordinate(2,2,0)
    myMaze.addCoordinate(3,2,0)
    myMaze.addCoordinate(4,2,0)
    myMaze.addCoordinate(6,2,0)
    myMaze.addCoordinate(7,2,0)
    myMaze.addCoordinate(4,3,0)
    myMaze.addCoordinate(7,3,0)
    myMaze.addCoordinate(4,4,0)
    myMaze.addCoordinate(7,4,0)
    myMaze.addCoordinate(3,5,0)
    myMaze.addCoordinate(4,5,0)
    myMaze.addCoordinate(7,5,0)
    myMaze.addCoordinate(1,6,0)
    myMaze.addCoordinate(2,6,0)
    myMaze.addCoordinate(3,6,0)
    myMaze.addCoordinate(4,6,0)
    myMaze.addCoordinate(5,6,0)
    myMaze.addCoordinate(6,6,0)
    myMaze.addCoordinate(7,6,0)
    myMaze.addCoordinate(5,7,0)
    myMaze.printMaze()
    print("The route from (1,0) to (3,6) found by the greedy algorithm is", myMaze.findRoute(1,0,3,6))
    print("The route from (1,0) to (3,6) found by the depth first search is", myMaze.findRouteDepth(1,0,3,6))

def main():
    mazeTest()


if(__name__ == "__main__"):
    main()