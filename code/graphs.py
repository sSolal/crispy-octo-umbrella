import random
import networkx as nx
import matplotlib.pyplot as plt

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
		self.nb_nodes = Nb_nodes
		self.nodes =  [i for i in range(Nb_nodes)]
		self.s = 0
		self.t = Nb_nodes-1
		self.edges = []
		    
	def add_edge(self, u, v, a, b):
		new_edge = Edge(u, v, a, b)
		self.edges.append(new_edge)

	def print_graph(self):
		for edge in self.edges :
		    print(edge)
		    
	def visualize_graph(self):
		G = nx.DiGraph()
		for i in self.nodes :
			G.add_node(i)
		for e in self.edges:
			G.add_edge(e.u, e.v)

		# Create a list of colors for the nodes
		node_colors = ['green' if i == 0 else 'red' if i == self.nb_nodes - 1 else 'blue' for i in G.nodes()]
		nx.draw(G, with_labels=True, font_weight='bold', node_color=node_colors)
		plt.show()
		    
	def eval(self, genom):
		weights = genom.weights
		pass

	def out_edges(self, node):
		return [e for e in self.edges if e.u == node]
