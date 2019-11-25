""" Code doc """
import random


class Code():

    def __init__(self):

        # brain is split in "cubes". Neurons in same cube are of the same type.

        self.brain = {
            "dimensions": (2, 2, 2),  # brain size in cubes.
            "structure": [0, 0, 0, 0, 0, 0, 0, 0]  # neuron type for each cube
        }

        self.neuron_types = [
            {
                "density": 1,  # neurons in each cell
                "synapses": 5,
                # probability of having dendron_length of 0, 1, 2 cubes.
                "dendron_length": [0.5, 0.3, 0.2],  # does not have to be normalized, but each must be <1.
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
        print('code:', self.encode())
        print('\t brain:', self.brain)
        print('\t neurons:', self.neuron_types)
