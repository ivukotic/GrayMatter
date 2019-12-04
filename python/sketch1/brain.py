""" brain doc """
import random
import math
import threading
import logging
from tkinter import Tk, Canvas

from code import Code
from neuron import Neuron, Synapse

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )


class Brain(threading.Thread):

    actions = []  # class variable. used to return
    """ for now simply add neurons. later this will need GA birth from two parents."""

    def __init__(self, name, gencode, start_event, continue_event):
        threading.Thread.__init__(self, group=None, target=None, name=name)
        print('creating brain', name)
        self.name = name
        self.start_event = start_event
        self.continue_event = continue_event
        self.neurons = []
        self.code = gencode.brain
        self.dimensions = self.code['dimensions']
        self.structure = self.code['structure']
        self.neuron_types = gencode.neuron_types

        self.food = 128
        self.age = 0
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

        # adding synapses
        n_neurons = len(self.neurons)
        for isn, source_neuron in enumerate(self.neurons):
            sc = source_neuron.cube
            for _syn in range(source_neuron.code['synapses']):
                while(True):
                    idn = random.randint(0, n_neurons - 1)
                    if idn == isn:  # avoids self-loops. larger loops are OK
                        continue

                    # synapse length is given by cieling of distance between cubes.
                    destination_neuron = self.neurons[idn]
                    dc = destination_neuron.cube
                    distance = math.ceil(pow(
                        (dc[0] - sc[0]) * (dc[0] - sc[0]) +
                        (dc[1] - sc[1]) * (dc[1] - sc[1]) +
                        (dc[2] - sc[2]) * (dc[2] - sc[2]), 0.5))
                    prob_conn = random.random()
                    if prob_conn > source_neuron.code['dendron_length'][distance]:
                        continue

                    source_neuron.add_synapse(
                        Synapse(destination_neuron, weight=random.random(), distance=distance)
                    )
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
        while True:
            self.start_event.wait(5)
            if not self.start_event.isSet():
                break  # to kill the thread.

            self.age += 1

            # add activation to the first two neurons.
            self.neurons[0].addInput(0.3)  # THIS IS WHAT EYES SEE?
            self.neurons[1].addInput(0.3)
            for neuron in self.neurons:
                neuron.tick()
            # get direction from output of last 2 neurons.
            self.direction = [self.neurons[-1].output, self.neurons[-2].output]
            self.food -= 1
            # report what's the current quality. Maybe it shoudl be more than that.
            Brain.actions.append(self.food)

            self.continue_event.wait()

    def print(self):
        logging.debug('>>> age:' + str(self.age) + '\tquality:' + str(self.getQuality()))
        # logging.debug('position:', self.getPosition(), '\tdirection:', self.getMove())
        # for neuron in self.neurons:
        # neuron.print()
