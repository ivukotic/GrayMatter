""" synapse doc """

from code import Code


class Synapse:
    """ """

    def __init__(self, neuron, weight, distance=1, sensitivity_decay=0.95):
        """ doc """
        self.neuron = neuron
        self.distance = distance
        self.weight = weight
        self.current_sensitivity = 1
        self.sensitivity_decay = sensitivity_decay

    def process(self, signal):

        return signal * self.weight


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

    def addInput(self):
        return

    def getOutput(self):
        return 0

    def tick(self):

        pass
