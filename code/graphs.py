import random

class Edge :
    def __init__(self, u, v, a=0, b=0):
        self.a = a  # t = a*d + b with d the flow of driver (nb / min)
        self.b = b
        self.u = u # u the starting node
        self.v = v # v the ending node
        
    def __repr__(self):
        return str(self.u)+" -> "+str(self.v)

class Graph : # a graph with weights
    def __init__(self, Nb_nodes):
            self.nodes =  [i for i in range(Nb_nodes)]
            self.s = 0
            self.t = Nb_nodes-1
            self.edges = []
            self.weight = {} # edge -> float [0, 1]
            
    def add_edge(self, u, v, a, b):
        new_edge = Edge(u, v, a, b)
        self.edges.append(new_edge)
        self.weight[new_edge] = 1
        
    def random_weights(self):
        for edge in self.edges :
            self.weight[edge] = random.random()
    
    def print_graph(self):
        for edge in self.edges :
            print(edge, ', w =', round(self.weight[edge], 2))
            
    def eval(self):
	pass

    def out_edges(self, node):
        return [e for e in self.edges if e.u == node]
