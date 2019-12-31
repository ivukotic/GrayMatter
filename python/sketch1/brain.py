""" brain doc """
import random
import math
import threading
import logging

from code import Code
from neuron import Neuron
from synapse import Synapse
import configuration as conf

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )


class Brain(threading.Thread):
    """ 
    segmented in 3D cubes. Each cube can contain single neuron type.
    for now simply add neurons. later this will need GA birth from two parents.
    """
    actions = []  # class variable. used to return

    def __init__(self, ID, gencode, start_event, continue_event):
        threading.Thread.__init__(self, group=None, target=None, name=str(ID))
        print('creating brain', ID)
        self.ID = ID
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

    def __str__(self):
        return "B" + str(self.ID)

    def generate_neurons(self):
        # done cube by cube
        cell = 0
        ni = 0
        for _i in range(self.dimensions[0]):
            for _j in range(self.dimensions[1]):
                for _k in range(self.dimensions[2]):
                    ntype_code = self.neuron_types[self.structure[cell]]
                    for _d in range(ntype_code['density']):
                        self.neurons.append(Neuron(ni, ntype_code, [_i, _j, _k]))
                        ni += 1
                    cell += 1

        # adding synapses
        n_neurons = len(self.neurons)
        for isn, source_neuron in enumerate(self.neurons):
            sc = source_neuron.cube
            for syn in range(source_neuron.code['synapses']):
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
                        Synapse(syn, destination_neuron, weight=random.random(), distance=distance)
                    )
                    break

    def getQuality(self):
        """ should return quality when asked by other brains. for start just food reserve. """
        return self.food

    def getPosition(self):
        return self.position

    def setPosition(self, position):
        self.position = position

    def getMove(self):
        vx = self.direction[0] / conf.Neuron['max_activation'] * conf.Brain['max_velocity']
        vy = self.direction[1] / conf.Neuron['max_activation'] * conf.Brain['max_velocity']
        return [vx, vy]

    def process_response(self, reward, view):
        self.food += reward
        # add activation to the first two neurons.
        self.neurons[0].addInput(view[0])
        self.neurons[1].addInput(view[1])

    def removeNeurons(self):
        return

    def run(self):
        while True:
            self.start_event.wait(5)
            if not self.start_event.isSet():
                break  # to kill the thread.

            self.age += 1

            for neuron in self.neurons:
                neuron.tick()
            # get direction from output of last 2 neurons.
            self.direction = [self.neurons[-1].output, self.neurons[-2].output]
            self.food -= 1
            # report what's the current quality. Maybe it should be more than that.
            Brain.actions.append(self.food)

            self.continue_event.wait()
            self.print_out()

    def print_out(self):
        bi, blevel = conf.print_opt['Brain']
        if bi == self.ID and blevel > 0:
            logging.debug('BRAIN ' + str(self) +
                          '\tage:' + str(self.age)
                          + '\tquality:' + str(self.getQuality())
                          + '\tposition:' + str(self.getPosition())
                          + '\tdirection:' + str(self.getMove()))
            ni, _nlevel = conf.print_opt['Neuron']
            for n in ni:
                self.neurons[n].print_out()

    def print_detailed(self):
        for neuron in self.neurons:
            neuron.print_detailed()
