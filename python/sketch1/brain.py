""" brain doc """
import random
import math
import threading
import logging

from code import Code
from neuron import Neuron, Synapse


logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )


class Brain(threading.Thread):

    """ for now simply add neurons. later this will need GA birth from two parents."""

    def __init__(self, name, gencode, time_event):
        threading.Thread.__init__(self, group=None, target=None, name=name)
        print('creating brain', name)
        self.name = name
        self.time_event = time_event
        self.neurons = []
        self.code = gencode.brain
        self.dimensions = self.code['dimensions']
        self.structure = self.code['structure']
        self.neuron_types = gencode.neuron_types

        self.food = 128
        self.position = (0, 0)
        self.direction = [random.randint(0, 1), random.randint(0, 1)]
        self.generate_neurons()

    def generate_neurons(self):
        # done cube by cube
        cell = 0
        for _i in range(self.dimensions[0]):
            for _j in range(self.dimensions[1]):
                for _k in range(self.dimensions[2]):
                    ntype_code = self.neuron_types[self.structure[cell]]
                    for _d in range(ntype_code['density']):
                        self.neurons.append(Neuron(ntype_code, [_i, _j, _k]))
                    cell += 1

        # synapse length is given by cieling of distance between cubes.
        n_neurons = len(self.neurons)
        for isn, source_neuron in enumerate(self.neurons):
            sc = source_neuron.cube
            for syn in range(source_neuron.code['synapses']):
                while(True):
                    idn = random.randint(0, n_neurons - 1)
                    if idn == isn:
                        continue
                    destination_neuron = self.neurons[idn]
                    dc = destination_neuron.cube
                    distance = math.ceil(pow(
                        (dc[0] - sc[0]) * (dc[0] - sc[0]) +
                        (dc[1] - sc[1]) * (dc[1] - sc[1]) +
                        (dc[2] - sc[2]) * (dc[2] - sc[2]), 0.5))
                    prob_conn = random.random()
                    if prob_conn > source_neuron.code['dendron_length'][distance]:
                        continue
                    source_neuron.add_synapse(Synapse(destination_neuron, weight=random.random()))
                    break

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

    def run(self):
        self.time_event.wait()
        while self.time_event.isSet():
            logging.debug('ticking...')
            self.neurons[0].addInput()
            for n in self.neurons:
                n.tick()
            self.direction = [self.neurons[-1].getOutput(), self.neurons[-2].getOutput()]
            self.food -= 1

    def prnt(self):
        print('q', self.getPosition(), self.getQuality())
