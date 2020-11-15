#usr/bin/python3

from collections import deque       #used to add/remove from beginning or end of list
from math import inf    #used as default distance between routers
from pandas import DataFrame

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
    #used to make sure edge is removed for all routers
    @property
    def nodes(self):
        nodes = sum(([edge.start, edge.end] for edge in self.edges),[]) #all nodes, [] makes sure to return 1 list
        return set(nodes)

    @property
    def neighbours(self):
        neighbours = {node: set() for node in self.nodes}    #dict comprehension creates empty set for each node, e.g {"a":set()}
        [neighbours[edge.start].add((edge.end, edge.cost)) for edge in self.edges]
        return neighbours       #returns dict with node and set of all neighbours with costs e.g. {"a": {("f",10),("b",9)}}

    #dijkstra's algorithm
    def dijkstra(self, source, dest):
        assert source in self.nodes, "Source not in graph\n"     #make sure source is in graph
        distances = {node: inf for node in self.nodes}       #set default distance to inf e.g {"a":inf}
        previous_nodes = {node: None for node in self.nodes}  #set default value to None e.g {"a":None}
        distances[source] = 0       #make sure value to itself is 0
        nodes = self.nodes.copy()     #to avoid altering self.nodes

        while nodes:
            current = min(nodes, key=lambda node: distances[node])    #returns node with shortest distance
            nodes.remove(current)     #make sure not to return to already visited node
            
            if distances[current] == inf:    #unable to reach
                break           
            
            for neighbour, cost in self.neighbours[current]:     
                alternative_path = distances[current] + cost    
                if alternative_path < distances[neighbour]:        #check if new distance is less than previous distance
                    distances[neighbour] = alternative_path            #change route
                    previous_nodes[neighbour] = current

        path = deque()
        current = dest
        while previous_nodes[current] is not None:        #going full circle
            path.appendleft(current)         #append to top of list
            current = previous_nodes[current]
        
        if path:        #if there is a path
            path.appendleft(current)

        #change total distance from inf to 0 or from float to int
        total_distance = 0
        if distances[dest] != inf:
            total_distance = int(distances[dest])

        return "->".join(list(path)),total_distance

class Router:
    def __init__(self,name,graph):
        self.name = name
        self.graph = graph

    def get_path(self,dest):
        path,cost = self.graph.dijkstra(self.name,dest)
        print("Start: {}".format(self.name))
        print("End: {}".format(dest))
        print("Path: {}".format(path))
        print("Cost: {}\n".format(cost))

    #create dataframe
    def print_routing_table(self):
        nodes = [node for node in self.graph.nodes if node != self.name]    #all nodes except current
        data = {"from": [self.name]* (len(self.graph.nodes)-1),        #-1 because we do not need self.name -> self.name
                "to": nodes,
                "cost": [self.graph.dijkstra(self.name,node)[1] for node in nodes],
                "path": [self.graph.dijkstra(self.name,node)[0] for node in nodes]}
        df = DataFrame(data,columns=["from","to","cost","path"])
        print(df)

    #remove all pairs with router
    def remove_router(self,router):
        self.graph.edges = [edge for edge in self.graph.edges if edge.start != router if edge.end != router]

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

    #2 routers
    router = Router("a",graph)
    router_two = Router("b",graph)

    #print tables
    router.print_routing_table()
    router_two.print_routing_table()
    
    #remove "c" router
    router.remove_router("c")

    #check it is removed from both
    router.print_routing_table()
    router_two.print_routing_table()

#comment out below to run unit test
if __name__ == main():
    main()