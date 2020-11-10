from collections import deque       #used to remove from beginning or end of list
from math import inf    #used as default distance between routers

class Edge:

    def __init__(self,start,end,cost):
        self.start = start
        self.end = end
        self.cost = cost

class Graph:
    
    def __init__(self):
        self.edges = []

    def add_edge(self,start,end,cost):
        edge = Edge(start,end,cost)
        self.edges.append(edge)

    #properties are made as they will need to be updated later, work like getter functions
    @property
    def vertices(self):
        return set(sum(([edge.start, edge.end] for edge in self.edges),[]))     #set of all nodes

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}    #dict comprehension creates set for each node, e.g {"a":set()}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours       #returns dict with node and set of all neighbours with costs e.g. {"a": {("f",10),("b",9)}}

    #dijkstra's algorithm
    def dijkstra(self, source, dest):
        assert source in self.vertices, "Source not in graph\n"     #make sure source is in graph
        distances = {vertex: inf for vertex in self.vertices}       #set default distance to inf e.g {"a":inf}
        previous_vertices = {vertex: None for vertex in self.vertices}  #set default value to None e.g {"a":None}
        distances[source] = 0       #make sure value to itself is 0
        vertices = self.vertices.copy()     #to avoid altering self.vertices

        while vertices:
            current_vertex = min(vertices, key=lambda vertex: distances[vertex])    #returns vertex with shortest distance
            vertices.remove(current_vertex)     #make sure not to return to already visited vertex
            
            if distances[current_vertex] == inf:    #unable to reach
                break           
            
            for neighbour, cost in self.neighbours[current_vertex]:     
                alternative_route = distances[current_vertex] + cost    
                if alternative_route < distances[neighbour]:        #check if new distance is less than previous distance
                    distances[neighbour] = alternative_route            #change route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:        #going full circle?
            path.appendleft(current_vertex)         #append to top of list
            current_vertex = previous_vertices[current_vertex]
        
        if path:        #if there is a path
            path.appendleft(current_vertex)

        return list(path),distances[dest]

class Router:

    def __init__(self,name,graph):
        self.name = name
        self.graph = graph

    def get_path(self,dest):
        path,cost = self.graph.dijkstra(self.name,dest)
        print("Start: {}".format(self.name))
        print("End: {}".format(dest))
        print("Path: {}".format("->".join(path)))
        print("Cost: {}\n".format(cost))

def main():
    graph = Graph()
    graph.add_edge("a", "b", 7)
    graph.add_edge("a", "c", 9)
    graph.add_edge("a", "f", 14)
    graph.add_edge("b", "c", 10)
    graph.add_edge("b", "d", 15)
    graph.add_edge("c", "d", 11)
    graph.add_edge("c", "f", 2)
    graph.add_edge("d", "e", 6)
    graph.add_edge("e", "f", 9)
    router = Router("a",graph)

    router.get_path("f")

if __name__ == main():
    main()