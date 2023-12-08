import matplotlib.pyplot as plt
from graphs import Graph
from algo_gen import Genom
from car_experimentation import experimentation
from car_simulation import fitness

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

expe_result = []
simu_result = []
abscisses = []

f = lambda i : 1+i

try:
    for i in range(30):
        abscisses.append(f(i))
        expe_result.append(experimentation(network, genom, delay=100, flow=f(i), simulation_length=1000, debug=False))
        simu_result.append(fitness(network, genom, flow=f(i)))
        print(" .",i, end="", flush=True)
except KeyboardInterrupt:
    print("Okay")
    l = min(len(expe_result), len(simu_result))
    expe_result = expe_result[:l]
    simu_result = simu_result[:l]
    abscisses = abscisses[:l]
plt.plot(abscisses, expe_result, label="experimentation")
plt.plot(abscisses, simu_result, label="simulation")
plt.legend()
plt.show()