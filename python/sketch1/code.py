""" Code doc """
import random


class Code():

    def __init__(self):

        # brain is split in "cubes". Neurons in same cube are of the same type.

        self.brain = {
            "dimensions": (2, 2, 2),  # brain size in cubes.
            "interconnectedness": .9,
            "structure": [0, 0, 0, 0, 0, 0, 0, 0]  # neuron type for each cube
        }

        self.neuron_types = [
            {
                "density": 1,  # neurons in each cell
                "leakage": 1,
                "random_signal_probability": .0001
            }
        ]

    def initial_generation(self):
        pass

    def encode(self):
        # encodes itself into a string and returns it.
        pass

    def decode(self, gencode):
        # decodes and initializes itself from gencode string.
        pass

    def crossover(self, foreign_code):
        pass

    def mutate(self):
        pass

    def prnt(self):
        print('code:', self.gencode)
        print('\t brain:', self.brain)
        print('\t neurons:', self.neuron)
