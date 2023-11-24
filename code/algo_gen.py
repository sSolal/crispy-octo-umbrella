from graphs import Graph
import random
import numpy as np
import matplotlib.pyplot as plt

class Genom:
	""" 
	A Genom is an individual of the Genetic Algorithm, ie a repartition of weights on the edges of a graph
	
	- self.n : the number of weights = the number of edges
	- self.weights : list of n POSITIVE numbers
	"""
	def __init__(self, n, weights=[]):
		self.n=n
		if weights==[]:	# If the weights are not already given
			self.random_genom()
		else:		# Otherwise
			self.weights=weights
		assert self.n == len(self.weights)

	def random_genom(self):
		weights = []
		for i in range(self.n):
		    weights.append(random.random())	# random between 0 et 1
		self.weights = weights

	def mutate_proba(self, proba_mutation = 0.1):
		new_weights = self.weights.copy()
		for i in range(self.n):
		    if random.random() < proba_mutation : 
		        new_weights[i] = min(1, max(0.01,  new_weights[i] + random.gauss(0,1)))
		return Genom(self.n, new_weights)
		        
	def mutate_choose_one(self):
		new_weights = self.weights.copy()
		i = random.randint(0, self.n-1)
		new_weights[i] =  min(1, max(0.01,  new_weights[i] + random.gauss(0,1)))
		return Genom(self.n, new_weights)

	def mutate_swap(self):
		new_weights = self.weights.copy()
		i = random.randint(0, self.n-1)
		j = i
		while j != i :
		    j = random.randint(0, self.n-1)
		new_weights[i], new_weights[j]=new_weights[j], new_weights[i]
		return Genom(self.n, new_weights)
		                       
	def cross_over(self, other):
		new_weights = []
		assert self.n == other.n 
		for i in range(self.n):
		    if random.random() < 0.5 :
		        new_weights.append(self.weights[i])
		    else :
		        new_weights.append(other.weights[i])
		return Genom(self.n, new_weights)
		                      
	def evaluate_on(self, G):  # Return the value of the fitness function for one individual (how he performs on the graph G)
		return G.eval_simple(self)
                              
class Population:
	""" 
	A Population is a list of individuals of the Genetic Algorithm

	- self.G : the graph to find the best weights in
	- self.nb_indiv : the number of individuals (TODO : compute nb_indiv depending on the number of edges of the graph)
	- self.pop : the list of Genom object
	- self.nb_edge = the number of edges in the graph G
	"""
	def __init__(self, G, N):
		self.G = G
		self.nb_indiv = N
		self.pop=[]
		self.nb_edge = len(self.G.edges)
		for i in range(self.nb_indiv):
		    self.pop.append(Genom(self.nb_edge))

	def evaluate_pop(self):
		dict_eval = {}
		for ind in self.pop :
		    dict_eval[ind] = ind.evaluate_on(self.G)
		sorted_pop = sorted(self.pop, key = lambda x : dict_eval[x])
		return sorted_pop, dict_eval[sorted_pop[0]]
		                      
	def train(self, Nb_generations, part_mut = 0.1, plot = True):
		nb_mut = int(self.nb_indiv*part_mut)
		nb_enfant = self.nb_indiv - nb_mut - 1
		all_bests = []
		better_bests = []
		best_solution = np.inf
		for i in range(1, Nb_generations+1):
		    sp, best_perf = self.evaluate_pop()
		    all_bests.append(best_perf)
		    if best_perf < best_solution :
		    	better_bests.append((best_perf, i))
		    	best_solution = best_perf
		    	
		    new_gen = [] # build the new_generation
		    new_gen.append(sp[0])
		    for j in range(nb_mut):
		    	new_gen.append( sp[j].mutate_choose_one() )
		    for j in range(nb_enfant):
		    	parent1 = sp[ int(0 + random.gauss(0, 1)) ]
		    	parent2 = parent1
		    	while parent2 == parent1 :
		    		parent2 = sp[int(1 + random.gauss(0, 2)) ]
		    	enfant = parent1.cross_over(parent2)
		    	new_gen.append(enfant)
		    	
		    self.pop = new_gen
		    
		if plot :
			plt.plot(all_bests)
			plt.show()
		return self.pop
		
		    
		    
# P = Genom(10)
# enfant = P.mutate()
