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


class Synapse:
    """ """

    def __init__(self, ID, neuron, weight, distance=1, sensitivity_decay=0.95):
        """ doc """
        self.ID = ID
        self.neuron = neuron  # destination neuron
        self.distance = distance
        self.weight = weight
        self.current_sensitivity = 1
        self.sensitivity_decay = sensitivity_decay
        self.pipeline = [0] * distance  # for pipeline to work each tick must call signal once

    def __str__(self):
        return "S" + str(self.ID)

    def signal(self, signal):
        self.pipeline.append(signal * self.weight)

    def process(self):
        signal = self.pipeline.pop(0) * self.current_sensitivity
        self.neuron.addInput(signal)

    def print_out(self):
        si, level = conf.print_opt['Synapse']
        if si == self.ID and level > 0:
            print('SYNAPSE {} dest:{}  distance:{:d}  weight:{:6.3f} sensit: {:6.3f} pipe:{}'.format(
                self, self.neuron, self.distance, self.weight, self.current_sensitivity, self.pipeline))

    def print_detailed(self):
        print('SYNAPSE {} dest:{}  distance:{:d}  weight:{:6.2f} sensit: {:6.2f} pipe:{}'.format(
            self, self.neuron, self.distance, self.weight, self.current_sensitivity, self.pipeline))
