from simpy import Environment, RealtimeEnvironment
from graphs import Graph
import random
# The network is a succession of ressources

REALTIME = True
NB_CARS = 10

Env = RealtimeEnvironment if REALTIME else Environment



def car(env, id, graph, road_use):
    current = 0

    while current != len(graph.nodes)-1:
        next_road = random.choice(graph.out_edges(current))
        road_use[next_road]+=1
        travel_time = next_road.a + road_use[next_road]*next_road.b  # Simulate random travel time
        print(id, "is going to", next_road.v, "We will be ", road_use[next_road], "on the road... It should take", str(travel_time)+"s")
        yield env.timeout(travel_time)
        road_use[next_road]-=1
        current = next_road.v


def experimentation ():
	print("Hello World")

	NB_CITIES = 4
     
	
	G = Graph(NB_CITIES)
	G.add_edge(0, 1, 2, 1)
	G.add_edge(1, 3, 5, 0)
	G.add_edge(0, 2, 2, 1)
	G.add_edge(2, 3, 5, 0)
     
	road_use = {e:0 for e in G.edges}#How many cars are on a given road


	env = Env()
	for i in range(NB_CARS):
		env.process(car(env, "Car "+str(i), G, road_use))
	env.run(until=10)

if __name__=="__main__":
     experimentation()