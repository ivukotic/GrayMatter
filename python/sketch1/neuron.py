"""
Neurons have synapses. Synapses describe destination Neuron, its distance, weight.
Neuron has a simple input that sums up signals, so there is nothing to process inputs.
On each tick, thresholded input is given to output and input maybe reset.
Once output is calculated, it is given to all the synapses. synapses put in it a pipeline,
add current signal to its neuron.
"""

""" synapse doc """

from code import Code


class Synapse:
    """ """

    def __init__(self, neuron, weight, distance=1, sensitivity_decay=0.95):
        """ doc """
        self.neuron = neuron  # destination neuron
        self.distance = distance
        self.weight = weight
        self.current_sensitivity = 1
        self.sensitivity_decay = sensitivity_decay
        self.pipeline = [0] * distance  # for pipeline to work each tick must call signal once

    def signal(self, signal):
        self.pipeline.append(signal * self.weight)

    def process(self):
        signal = self.pipeline.pop(0) * self.current_sensitivity
        self.neuron.addInput(signal)

    def print(self):
        pass
        print('syn:', self.distance, self.weight, self.current_sensitivity, self.pipeline)


class Neuron:
    """ """

    def __init__(self, gencode, cube):
        self.code = gencode
        self.cube = cube
        self.current_threshold = 128
        self.leakage = gencode["leakage"]
        self.random_signal_probability = gencode["random_signal_probability"]
        self.synapses = []
        self.input = 0
        self.output = 0

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
            synapse.signal(self.output)

    def tick(self):
        self.calculate_output()
        self.generate_outputs()

    def print(self):
        print('cube', self.cube, self.input, self.output)
        for synapse in self.synapses:
            synapse.print()
