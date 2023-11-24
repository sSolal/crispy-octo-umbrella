from graphs import Graph
import random

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
		        new_weights[i] = min(1, max(0,  new_weights[i] + random.gauss(0,1)))
		return Genom(self.n, new_weights)
		        
	def mutate_choose_one(self):
		new_weights = self.weights.copy()
		i = random.randint(0, self.n-1)
		new_weights[i] =  min(1, max(0,  new_weights[i] + random.gauss(0,1)))
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
		pass
                              
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
		    dict_eval[ind] = ind.evaluate_on(G)
		sorted_pop = sorted(self.pop, key = lambda x : dict_eval[x])
		return sorted_pop
		                      
	def train(self, Nb_generations):
		for i in range(1, Nb_generations+1):
		    sp = self.evaluate_pop()
		    # build the new_generation

# P = Genom(10)
# enfant = P.mutate()
