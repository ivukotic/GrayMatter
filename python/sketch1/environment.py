import random
import math
import pandas as pd
import numpy as np
import configuration as conf
from vizualize import platno


class Environment:
    def __init__(self, size_x=conf.Universe["size_x"], size_y=conf.Universe['size_y']):
        self.size_x = size_x
        self.size_y = size_y
        self.display = platno("Environment", self.size_x, self.size_y)
        self.init()

    def init(self):

        # self.display.setTitle("Environment")
        # self.display.setSize(self.size_x, self.size_y)

        if conf.Environment['model'] == 0:
            self.food = pd.DataFrame(np.fromfunction(lambda x, y: x * 2 + y * 2, [self.size_x, self.size_y]))
        else:
            self.food = pd.DataFrame(0, index=range(self.size_x), columns=range(self.size_y))

        if conf.Environment['model'] == 1:
            for i in range(10):
                x1 = random.randint(0, self.size_x / 2)
                x2 = random.randint(0, self.size_x / 2)
                y1 = random.randint(0, self.size_y / 2)
                y2 = random.randint(0, self.size_y / 2)
                am = 10000 / math.fabs((x1 - x2) + 1 * (y1 - y2) + 1)
                self.food.loc[x1:x2, y1:y2] = am

    def get_response(self, position, direction):
        (x, y) = position
        (dx, dy) = direction

        x = int(x)
        y = int(y)
        reward = self.food[x][y]
        self.food.loc[x, y] = 0

        nx = x + dx
        ny = y + dy
        if nx >= self.size_x:
            nx = self.size_x - 1
        elif nx <= 0:
            nx = 0
        if ny >= self.size_y:
            ny = self.size_y - 1
        elif ny <= 0:
            ny = 0
        new_pos = [nx, ny]

        # view is sum of five cells in direction -30 deg and +30 deg
        tan_dir = 1
        if dx != 0:
            tan_dir = dy / dx
        dire = math.atan(tan_dir)
        dir1 = dire - 0.52
        dir2 = dire + 0.52
        dx1 = math.cos(dir1)
        dy1 = math.sin(dir1)
        dx2 = math.cos(dir2)
        dy2 = math.sin(dir2)
        view = [0, 0]
        for i in [0, 1, 2, 3, 4]:
            lx = int(x + dx1 * i)
            ly = int(x + dy1 * i)
            if lx < 0 or lx >= self.size_x or ly < 0 or ly >= self.size_y:
                break
            view[0] += self.food[lx][ly]

            lx = int(x + dx2 * i)
            ly = int(x + dy2 * i)
            if lx < 0 or lx >= self.size_x or ly < 0 or ly >= self.size_y:
                break
            view[1] += self.food[lx][ly]

        return [reward, new_pos, view]
