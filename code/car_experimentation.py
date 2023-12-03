from simpy import Environment, RealtimeEnvironment
from graphs import Graph
import random
from algo_gen import Genom
# The network is a succession of ressources

#Does the simulation run in realtime (useful to understand what is going on by printing infos)
REALTIME = False
Env = RealtimeEnvironment if REALTIME else Environment

#Flow of cars entering the network
CAR_FLOW = 4000 #Car per hour

#Time before measuring starts (waiting for the network to "fill")
DELAY_IN_MEASURE = 30

#Evaluation dampening
DECAY_FACTOR = 0.5 #Experimental. A low factor means that the simulation updates "quickly" the computed times, but it may be "jittery"
                   #              A high factor (close to 1) means that the simulation is slow to update, it dampens it but may lead to an under approximation of real times

#Simulation helpers

class SimulationState:
    def __init__(self, network, flow=CAR_FLOW, delay=DELAY_IN_MEASURE):
        self.cars_on_network = 0
        self.cars_on_road = {e:0 for e in network.edges} #How many cars are on each given road
        self.cross_time = {e:max(e.a, 1) for e in network.edges}#How long it takes (experimentally to cross the edge)

        self.total_travel_time = 0
        self.cars_measured = 0

        self.flow = flow
        self.delay = delay

        self.measure_started = False


    def flow_on_road(self, road):
        return self.cars_on_road[road]/self.cross_time[road] #The number of "cars per second" on the road at a given instant

    def update_cross_time(self, road, time):
        self.cross_time[road] = DECAY_FACTOR*self.cross_time[road] + (1-DECAY_FACTOR)*time

    def display(self):
        print(self.cars_on_network, "cars on the road !")

def coefficiented_choice(choices, coefs):
    # We choose a road, with a probability proportional to the coefficient
    total = sum(coefs)
    r = random.random()*total
    for i, c in enumerate(coefs):
        if r < c:
            return choices[i]
        r -= c

#Simulation pieces

def car(env, network, genom, simulation):
    current_city = 0
    travel_time = 0 #Accumulated during simulation

    measuring = simulation.measure_started #Is this car performance to be measured ?

    #Logging infos
    simulation.cars_on_network += 1

    while current_city != len(network.nodes)-1: #While we are not at destination (last city of the map)

        choices = network.out_edges(current_city)
        coefs = [genom.weights[network.edges.index(e)] for e in choices] #Could have written just "genom.weights[e] for e in choices" but it seems more robust like that
        
        road = coefficiented_choice(choices, coefs) #Choosing a road at random

        simulation.cars_on_road[road]+=1 # Entering the road

        cross_time = road.a + simulation.flow_on_road(road)*road.b #Applying our congestion formula
        travel_time += cross_time

        yield env.timeout(cross_time) # Road trippin'

        current_city = road.v # Arriving at destination

        simulation.cars_on_road[road]-=1 # Exiting the road

        #Updating the experimental "cross_time of the road"
        simulation.update_cross_time(road, cross_time)

    simulation.cars_on_network -= 1

    if measuring:
        simulation.total_travel_time += travel_time
        simulation.cars_measured += 1

def car_factory(env, network, genom, simulation):
    while True:
        new_car = car(env, network, genom, simulation)
        env.process(new_car)
        yield env.timeout(1/simulation.flow)

# We start measuring cars some time after the beginning of the simulation to allow the network to "fill up"
def delay_measure(env, simulation):
    yield env.timeout(simulation.delay)
    simulation.measure_started = True

# Regularly displays relevant infos so that we know what is happenning
def display_info(env, simulation, interval=2):
    while True:
        print("At time", env.now, end=" : ")
        simulation.display()
        yield env.timeout(interval)


def generate_network_braess(braess=False):
    network = Graph(4)
    if not braess:
        network.add_edge(0, 1, 0, 1/400)
        network.add_edge(1, 3, 15, 0)
        network.add_edge(0, 2, 15, 0)
        network.add_edge(2, 3, 0, 1/400)
        genom = Genom(4, [1,1,1,1])
    else:
        network.add_edge(0, 1, 0, 1/400)
        #network.add_edge(1, 3, 45, 0)
        network.add_edge(1, 2, 2, 0)
        #network.add_edge(0, 2, 45, 1)
        network.add_edge(2, 3, 0, 1/400)
        genom = Genom(3, [1,1,1])
    return network, genom


def experimentation (network, genom, delay = DELAY_IN_MEASURE, flow = CAR_FLOW, simulation_length = 100, debug=True):
    env = Env()
    simulation = SimulationState(network, flow = flow, delay = delay)

    #Launch all the processes to throw cars into the network and monitor
    if debug:
        env.process(display_info(env, simulation, 20))
    env.process(delay_measure(env, simulation))
    env.process(car_factory(env, network, genom, simulation))

    env.run(until=simulation_length)
    
    return simulation.total_travel_time/simulation.cars_measured

if __name__=="__main__":
    print("Experimentation without Braess's road")
    time = experimentation(*generate_network_braess())
    print("Average time :", time)
    print("Experimentation with Braess's road")
    time = experimentation(*generate_network_braess(True))
    print("Average time :", time)

    print("Justine's example")

    #Justine's example
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
    time = experimentation(network, genom, delay=100, flow=50, simulation_length=5000)
    print("Average time :", time)