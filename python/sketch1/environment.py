import random
import math
import pandas as pd
import numpy as np
import configuration as conf


class Environment:
    def __init__(self, size_x=conf.Universe["size_x"], size_y=conf.Universe['size_y']):
        self.size_x = size_x
        self.size_y = size_y
        self.food = pd.DataFrame(np.fromfunction(lambda x, y: x * 2 + y * 2, [self.size_x, self.size_y]))

    def get_response(self, position, direction):
        (x, y) = position
        (dx, dy) = direction
        reward = self.food[x][y]
        self.food[x][y] = 0
        # view is sum of five cells in direction -30 deg and +30 deg
        sin_dir = dy / dx
        dire = math.asin(sin_dir)
        dir1 = dire - 0.52
        dir2 = dire + 0.52
        dx1 = math.cos(dir1)
        dy1 = math.sin(dir1)
        dx2 = math.cos(dir2)
        dy2 = math.sin(dir2)
        view = [0, 0]
        for i in [0, 1, 2, 3, 4]:
            lx = x + dx1 * i
            ly = x + dy1 * i
            if lx < 0 or lx >= self.size_x or ly < 0 or ly >= self.size_y:
                break
            view[0] += self.food[lx][ly]

            lx = x + dx2 * i
            ly = x + dy2 * i
            if lx < 0 or lx >= self.size_x or ly < 0 or ly >= self.size_y:
                break
            view[1] += self.food[lx][ly]
        return [reward, view]
