from graphs import Graph
from random import randint

#Function that takes a graph and checks if there is a path between two nodes:
def is_path(graph, node1, node2):
    to_visit = [node1]
    while to_visit != []:
        node = to_visit.pop(0)
        if node == node2:
            return True
        to_visit += [e.v for e in graph.out_edges(node)]
    return False

def random_pop(liste):
    return liste.pop(randint(0,len(liste)-1))

def generate_dag(nb_nodes):
    # Initialize an empty graph
    graph = Graph(nb_nodes)

    for i in range(nb_nodes-1): #Every node except the last sink
        nb_out = randint(1, nb_nodes-i-1)
        candidates = list(range(i+1, nb_nodes))
        print(nb_out)
        for _ in range(nb_out):
            out = random_pop(candidates)
            graph.add_edge(i, out, 1, 1)

    for i in range(nb_nodes-1):
        if not is_path(graph, 0, i):
            graph.add_edge(0, i, 1, 1)
        if not is_path(graph, i, nb_nodes-1):
            graph.add_edge(i, nb_nodes-1, 1, 1)
        
        
    return graph

if __name__=="__main__":
    print("Generating a graph !")

    graph = generate_dag(4)
    graph.visualize_graph()
