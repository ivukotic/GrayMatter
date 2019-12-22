"""
Neurons have synapses. Synapses describe destination Neuron, its distance, weight.
Neuron has a simple input that sums up signals, so there is nothing to process inputs.
On each tick, thresholded input is given to output and input maybe reset.
Once output is calculated, it is given to all the synapses. synapses put in it a pipeline,
add current signal to its neuron.
"""

""" synapse doc """

from code import Code
import configuration as conf
from synapse import Synapse


class Neuron:
    """ """

    def __init__(self, ID, gencode, cube):
        self.ID = ID
        self.code = gencode
        self.cube = cube
        self.current_threshold = 128
        self.leakage = gencode["leakage"]
        self.random_signal_probability = gencode["random_signal_probability"]
        self.synapses = []
        self.input = 0
        self.output = 0

    def __str__(self):
        return "N" + str(self.ID)

    def add_synapse(self, synapse):
        self.synapses.append(synapse)

    def remove_synapse(self):
        pass

    def addInput(self, potential):
        self.input += potential

    def calculate_output(self):
        self.input -= self.leakage
        self.output = 0
        if self.input > self.current_threshold:
            self.output = self.input
            self.input = 0

    def generate_outputs(self):
        for synapse in self.synapses:
            synapse.process()
            synapse.signal(self.output)

    def tick(self):
        self.calculate_output()
        self.generate_outputs()

    def print_out(self):
        ni, nlevel = conf.print_opt['Neuron']
        if ni == self.ID and nlevel > 0:
            print('NEURON', self,
                  '\tposition:', self.cube,
                  '\tinput:', self.input,
                  '\toutput:', self.output)
            si, slevel = conf.print_opt['Synapse']
            self.synapses[si].print_out()

    def print_detailed(self):
        for synapse in self.synapses:
            synapse.print_out()
