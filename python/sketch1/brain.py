""" brain doc """
import random
from neuron import Neuron, Synapse

class Brain():

    """ for now simply add neurons. later this will need GA birth from two parents."""

    def __init__(self, name, n_neurons=5, interconnectedness=0.9):
        self.name = name
        self.neurons = []
        self.food = 128
        self.x = 0
        self.y = 0
        self.direction = [random.randint(0, 1), random.randint(0, 1)]
        self.interconnectedness = interconnectedness
        print('creating brain')

        for _i in range(n_neurons):
            self.neurons.append(Neuron())

        for _i in range(n_neurons):
            for _j in range(_i + 1, n_neurons):
                if random.random() > self.interconnectedness:
                    continue
                self.neurons[_i].add_synapse(Synapse(neuron=self.neurons[_j], weight=random.random()))

    def getQuality(self):
        """ should return quality when asked by other brains. for start just food reserve. """
        return self.food

    def getPosition(self):
        return self.x, self.y

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def addFood(self, food):
        self.food += food

    def getMove(self):
        return self.direction

    def removeNeurons(self):
        return

    def tick(self):
        self.neurons[0].addInput()
        for n in self.neurons:
            n.tick()
        self.direction = [self.neurons[-1].getOutput(), self.neurons[-2].getOutput()]
        self.food -= 1

    def prnt(self):
        print('q', self.getPosition(), self.getQuality())
