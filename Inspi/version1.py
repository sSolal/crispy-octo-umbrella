"""
Dans cette version, les trajets se font les uns après les autres donc sans embouteillages.
Ce que l'on cherche à optimiser est juste le nombre d'arête que l'on prend
DONE
"""

import numpy as np
import matplotlib.pyplot as plt
import random

def random_proba_distrib(n):	# return a random list of n number for wich the sum makes 1. If n = 0, then []
	if n == 0 :		# A voir si c'est vraiment si random que ça mais en tout cas ça marche pour l'instant
		return []
	if n == 1 :
		return [1]
	L = []
	for i in range(n):
		L.append(random.random())
	S = sum(L)
	for i in range(n):
		L[i] = round(L[i]/S, 4)
	return L

class Node :
	def __init__(self, nom):
		self.nom = nom
		self.voisins = []	# list of nodes that are accessible by self
		self.nb_voisins = 0	# number of nodes that are accessible by self
		self.edges_leaving = [] # list of edges that leave from self
		
	def display_voisins(self):
		print('liste de voisins de  ' + self.nom, end = ' : ')
		for v in self.voisins :
			print(v.nom, end = ' ')
		print()
		
class Edge :
	def __init__(self, u, v, cout = 1):
		self.u = u
		self.v = v
		self.cout = cout
		self.proba = 0
		
class Graph :	# directed graphs
	def __init__(self, nodes, edges):
		self.nodes = nodes
		self.edges = []
		self.start = self.nodes[0]	# start of the path
		self.terminal = self.nodes[-1]  # end of the path
		for (i,j) in edges :
			self.add_edge(i,j)
			
	def display_graph(self):
		for n in self.nodes :
			print('Node ' + n.nom + ' is adjacent to :', end = ' ') 
			n.display_voisins()
			
	def add_edge(self,i,j):	 # arete de i vers j
		u = self.nodes[i]
		v = self.nodes[j]
		e = Edge(u,v)
		self.edges.append(e)
		u.voisins.append(v)
		u.edges_leaving.append(e)
		u.nb_voisins += 1

class Strategy :
	def __init__(self, G, probas):
		self.G = G
		if probas == {} :
			probas = self.random_strategy()
		self.probas = probas
		
	def random_strategy(self):
		strat = {}
		for n in G.nodes :
			strat[n] = {}
			L = random_proba_distrib(n.nb_voisins)
			for i in range(n.nb_voisins) :
				strat[n][n.edges_leaving[i]] = L[i] # un nombre	dont la somme fait 1
		return strat
	
	def display_strat(self):
		for n in self.probas :
			print('En partant du noeud ' + n.nom + ' on peut aller vers : ')
			for e in self.probas[n] :
				print(e.v.nom + ' avec une proba de ' + str(self.probas[n][e]))
			print()
			
	def one_travel(self, display_path = False):		# Un parcours individuel de la strategie
		path = [G.start]
		actual_node = G.start
		iterations = 0
		while iterations < 100 :	# 100 pour l'instant pour le max d'iterations mais à changer plus tard si gros graphes
			possible_ways = self.probas[actual_node]
			if possible_ways == {} :	# si c'est un cul de sac
				break
			random_value = random.random() 	# entre 0 et 1
			value = 0
			for i in range(actual_node.nb_voisins) :
				value += possible_ways[actual_node.edges_leaving[i]]
				if random_value <= value :
					future_node = actual_node.edges_leaving[i].v
					break
			path.append(future_node)
			actual_node = future_node
			iterations += 1
			if future_node == G.terminal : 
				break
		if display_path :
			for n in path :
				print(n.nom, end = ' ')
			print()
		return(iterations)	# plus le score est petit, plus la strategie est bonne
	
	def evaluate_one_travel(self):	# 100 essais pour chaque evaluation
		N_tries = 100 
		score = 0
		for i in range(N_tries):
			score += self.one_travel()
		return score/N_tries
				
	def multiple_travel(self, N):	# Un parcours multiple à N agents de la strategie
		pass
		
	def evaluate_multiple_travel(self):
		pass
		
	def mutate(self, pm = 0.15):	# return another strategy with a mutation
		new_probas = {}
		for n in self.G.nodes :
			if random.random() < pm :	# if a mutation occurs
				new_probas[n] = {}
				L = random_proba_distrib(n.nb_voisins)	# We try differents probas
				for i in range(n.nb_voisins) :
					new_probas[n][n.edges_leaving[i]] = L[i] # dont la somme fait 1
			else :
				new_probas[n] = self.probas[n]
		return Strategy(G, new_probas)

	def criss_cross(self, other):	# return another strategy from a cross over of self and other
		new_probas = {}
		for n in self.G.nodes :
			if random.random() > 0.5 :
				new_probas[n] = self.probas[n]
			else :
				new_probas[n] = other.probas[n]
		return Strategy(G, new_probas)
	

		
class Population :
	def __init__(self, G, Nb_ind = 20):	# Voir si on peut faire en sorte qu'on puisse changer Nb_ind
		self.G = G
		self.pop = []
		for i in range(Nb_ind):
			self.pop.append(Strategy(G, {}))
				
				
	def fitness_evaluation(self):
		sorted_pop = sorted(self.pop, key = lambda x : x.evaluate_one_travel())
		return sorted_pop
    
	def evolution_step(self):
		sp = self.fitness_evaluation()
		new_pop = []
		new_pop.append(sp[0])   #garder le meilleur
		new_pop.append( sp[0].criss_cross(sp[1]) )  # 6 reproduction	(à changer avec des probas de mutations et tout)
		new_pop.append( sp[0].criss_cross(sp[2]) )
		new_pop.append( sp[1].criss_cross(sp[2]) )
		new_pop.append( sp[2].criss_cross(sp[3]) )
		new_pop.append( sp[1].criss_cross(sp[3]) )
		new_pop.append( sp[0].criss_cross(sp[3]) )
		new_pop.append( sp[0].mutate() )        # 4 mutations
		new_pop.append( sp[1].mutate() )
		new_pop.append( sp[2].mutate() )
		new_pop.append( sp[3].mutate() )
		for i in range(9):                      # 9 au pif
			new_pop.append(Strategy(self.G, {}))
		self.pop = new_pop
	
	def training(self, N0, plot = False):
		X = []
		for i in range(N0):
			self.evolution_step()
			X.append(self.pop[0].evaluate_one_travel())
		if plot :
			plt.plot(X)
			plt.xlabel('Nb generation')
			plt.ylabel('Score')
			plt.show()
		print("Training done")
		
	def perf_test(self):   # better after training
		sp = self.fitness_evaluation()
		best_strategy = sp[0]
		best_strategy.display_strat()
		print('Exemple de trajet aléatoire sur la meilleure stratégie : ')
		best_strategy.one_travel(display_path = True)
		print('Score de la meilleure stratégie : ')
		print(best_strategy.evaluate_one_travel())
		

if __name__ == '__main__':

	# Graph Def :
	
	nA = Node('A')
	nB = Node('B')
	nC = Node('C')
	nD = Node('D')
	nE = Node('E')
	nF = Node('F')
	nG = Node('G')
	
	G = Graph([nA, nB, nC, nD, nE, nF, nG], [(0, 1), (0, 2), 
						 (1, 2), (1, 3), (1, 4), 
						 (2, 1), (2, 3),
						 (3, 5), (3, 6),
						 (4, 3), (4, 5), 
						 (5, 3), (5, 6)])
			
	# Population of Strategy (Genetic Algorithm)			 
	
	P = Population(G)
	P.training(50, True)
	P.perf_test()
