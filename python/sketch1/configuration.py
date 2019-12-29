Universe = {
    "size_x": 200,
    "size_y": 200,
    "population_size": 10,
    "max_age": 9
}
viz = True  # show display

# list [index, debug level]. printed on each tick
print_opt = {
    "Universe": [0, 1],
    "Brain": [1, 1],
    "Neuron": [[0, 1, 2], 1],
    "Synapse": [4, 1]
}

# print full brain 0 at this tick
special_show_at = 10
