from graphs import Graph

class Genom:
	def __init__(self, n,weights=[]):
        self.n=n
        if weights==[]:
            self.weights=[1]*n
        else:
            self.weights=weights
            self.n=len(self.weights)

    def random_genom(self):
        for i in range(self.n):
            self.weight[i]=random.random()
	    
	def mutate(self):
	    pass#...

class Population:
    def __init__(self, G, N):
        self.G = G
        self.pop=[]
        for i in range(N):
            self.pop.append(Genom(len(self.G.edges)))

P = Genom(10)
enfant = P.mutate()