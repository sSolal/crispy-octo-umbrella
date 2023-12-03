import random
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

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
	
	def edge_index(self, edge):
		return self.edges.index(edge)

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
		nx.draw(G, with_labels=True, font_weight='bold', node_color=node_colors, node_size = 1000)
		plt.show()
		
	def visualize_genom(self, genom, label = True):	# Il faut que genom.weights et self.G.edges ait la même taille !!!
		G = nx.DiGraph()
		for i in self.nodes :
			G.add_node(i)
		#list_weighted_edges = []
		dico_edge_width = {}
		dico_label_edges = {}
		proba_weights = self.compute_proba(genom)
		for k,e in enumerate(self.edges) :
			i,j = e.u, e.v
			G.add_edge(i,j)
			w = round(proba_weights[e], 3)
			dico_label_edges[(i,j)] = str(w)
			dico_edge_width[(i,j)] = 1+5*w
			#list_weighted_edges.append((i,j,w))
		#G.add_weighted_edges_from(list_weighted_edges)
		pos = nx.planar_layout(G)
		# Create a list of colors for the nodes
		node_colors = ['green' if i == 0 else 'red' if i == self.nb_nodes - 1 else 'blue' for i in G.nodes()]
		nx.draw(G, pos, with_labels=True, font_weight='bold', node_color=node_colors, node_size = 1000)
		if label :
			nx.draw_networkx_edge_labels(G, pos, edge_labels = dico_label_edges, font_size=10, font_color='red')
		nx.draw_networkx_edges(G, pos,edgelist=G.edges(), width=[dico_edge_width[e] for e in G.edges()])
		plt.show()
		
	def random_traject(self, genom):
		dict_edges_weghted = { self.edges[i]: genom.weights[i] for i in range(genom.n) }
		chemin = [self.s]
		actual_node = self.s
		time = 0
		while actual_node != self.t :
			edges_possible = self.out_edges_weighted(actual_node, genom)
			edge_choosen = random.choices(list(edges_possible.keys()), weights=edges_possible.values(), k=1)[0]
			time += edge_choosen.b
			actual_node = edge_choosen.v
			chemin.append(actual_node)
		return chemin, time
				
	def eval_simple(self, genom):
		nb_trajects = 100
		S = 0
		for i in range(nb_trajects):
			chemin, time = self.random_traject(genom)
			S += time
		return S/100
		
	def out_edges_weighted(self, node, genom):
		return {self.edges[i] : genom.weights[i] for i in range(genom.n) if self.edges[i].u == node}
		
	def out_edges(self, node):
		return [e for e in self.edges if e.u == node]
		
	def compute_proba(self, genom): #compute the dico of probas {edge : proba} such that the sum of possible path is always 1
		probas = {}
		for node in range(self.nb_nodes):
			out_weights = self.out_edges_weighted(node, genom)
			total_weight = sum(out_weights.values())
			for e,w in out_weights.items():
				proba = w/total_weight
				probas[e] = proba
		return probas
		
	def compute_flow(self, probas):	#compute the dico of flow of driver {edge : flow}
	
		previous_edges = {n:[] for n in self.nodes}
		for e in self.edges :
			previous_edges[e.v].append(e)
		nb_edges_to_be_visited = {n : len(previous_edges[n]) for n in self.nodes}
		flows = {e:0 for e in self.edges}
		active_node = [self.s]
		while active_node != [] :
			node = active_node.pop(0)
			if node == 0 :
				total_flow_at_node = 1
			else :
				total_flow_at_node = 0
				for previous_e in previous_edges[node]:
					total_flow_at_node += flows[previous_e]
			for e in self.edges :
				if e.u == node :
					flow = probas[e] * total_flow_at_node
					flows[e] = flow
					nb_edges_to_be_visited[e.v] -= 1
					if nb_edges_to_be_visited[e.v] == 0:
						active_node.append(e.v)
		return flows

	def all_path(self): # return the list of paths from s to t (each path is a list of edges)	 !!!!! ACYCLIC DIRECTED GRAPH
		total_paths = []	# list of paths from s to t
		builded_paths = []
		for e in self.edges :
			if e.u == self.s :
				builded_paths.append([e])
		while len(builded_paths) != 0 :
			path = builded_paths.pop(0)
			actual_node = path[-1].v
			for e in self.edges :
				if e.u == actual_node :
					new_path = path.copy()
					new_path.append(e)
					if e.v == self.t :
						total_paths.append(new_path)
					else :
						builded_paths.append(new_path)
		return total_paths
			
