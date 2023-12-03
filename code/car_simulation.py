from graphs import Graph
from algo_gen import Genom
from graphs import Graph

# Computing the fitness function for a given network and genom

# Takes a genom and normalize the probabilities so that further calculations are correct
def normalize(network, genom):
    weights = genom.weights
    normalized_weights = weights[:]
    for i in range(network.nb_nodes):
        roads_from = network.out_edges(i)
        sum_of_weights = sum([weights[network.edge_index(road)] for road in roads_from])
        for road in roads_from:
            normalized_weights[network.edge_index(road)] /= sum_of_weights
    return normalized_weights


# Returns all pathes from source to destination as lists
def all_path(network): #Under the assumption that it is a DAG
    paths = []
    def aux(current, path):
        if current == network.nb_nodes-1:
            paths.append(path)
        else:
            for road in network.out_edges(current):
                aux(road.v, path+[road])
    aux(0, [])
    return paths


# Probability of a given path to be taken
def probability_of_path(network, normalized, path):
    proba = 1
    for road in path:
        proba *= normalized[network.edge_index(road)]
    return proba

# Return the expected flow of people on each section of road
def flow_on_edges(network, normalized, base_flow = 1):
    flows = [0]*len(network.edges)

    def aux(current, current_flow):
        if current != network.nb_nodes-1:
            for road in network.out_edges(current):
                flows[network.edge_index(road)] += current_flow*normalized[network.edge_index(road)]
                aux(road.v, current_flow*normalized[network.edge_index(road)])
    aux(0, base_flow)
    return flows

# Return the expected travel time on each section of road given the computed expected flow
def travel_times(network, flows):
    times = [0]*len(network.edges)
    for i, road in enumerate(network.edges):
        times[i] = road.a + flows[i]*road.b
    return times

def path_travel_times(network, path, times):
    return sum([times[network.edge_index(road)] for road in path])

def fitness(network, genom, flow):
    normalized = normalize(network, genom)
    paths = all_path(network)
    probas = [probability_of_path(network, normalized, path) for path in paths]
    flows = flow_on_edges(network, normalized, flow)
    times = travel_times(network, flows)
    path_times = [path_travel_times(network, path, times) for path in paths]
    return sum([probas[i]*path_times[i] for i in range(len(probas))])


if __name__=="__main__":
    network = Graph(6)
    network.add_edge(0, 1, 1, 1)
    network.add_edge(0, 2, 1, 1)
    network.add_edge(0, 4, 1, 1)
    network.add_edge(1, 3, 1, 1)
    network.add_edge(1, 5, 1, 1)
    network.add_edge(3, 5, 1, 1)
    network.add_edge(2, 4, 1, 1)
    network.add_edge(2, 3, 1, 1)
    network.add_edge(4, 5, 1, 1)

    genom = Genom(9, [3,2,5,3,7,1,2,8,1])
    print(fitness(network, genom, 50))