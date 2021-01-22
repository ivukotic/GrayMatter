
special_show_at = 10 # print full brain 0 at this tick
viz = True  # show display

Universe = {
    "size_x": 200,
    "size_y": 200,
    "population_size": 10,
    "max_age": 99
}

Environment = {
    "model": 1  # 0 - smooth gradient, 1- random squares
}

# list [index, debug level]. printed on each tick
print_opt = {
    "Universe": [0, 1],
    "Brain": [1, 1],
    "Neuron": [[0, 1, 2], 1],
    "Synapse": [4, 1]
}

Brain = {
    'max_velocity': 5
}

Neuron = {
    'max_activation': 255
}
