""" brain doc """
import random
from neuron import Neuron, Synapse
from code import Code


class Brain():

    """ for now simply add neurons. later this will need GA birth from two parents."""

    def __init__(self, name, gencode):
        print('creating brain', name)
        self.name = name
        self.neurons = []
        self.code = gencode.brain
        self.dimensions = self.code['dimensions']
        self.interconnectedness = self.code['interconnectedness']
        self.structure = self.code['structure']
        self.neuron_types = gencode.neuron_types

        self.food = 128
        self.position = (0, 0)
        self.direction = [random.randint(0, 1), random.randint(0, 1)]
        self.generate_neurons()

    def generate_neurons(self):
        # done cell by cell
        cell = 0
        for _i in self.dimensions[0]:
            for _j in self.dimensions[1]:
                for _k in self.dimensions[2]:
                    ntype_code = self.neuron_types[self.structure[cell]]
                    for _d in range(ntype_code['density']):
                        self.neurons.append(Neuron(ntype_code, [_i, _j, _k]))
                    cell += 1

        # synapse length is given by cieling of distance between cubes.
        for _i in range(self.neurons):
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
        return self.position

    def setPosition(self, x, y):
        self.position = (x, y)

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
