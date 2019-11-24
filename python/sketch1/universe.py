import random
import numpy as np
import pandas as pd
from brain import Brain
from code import Code
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['figure.figsize'] = [8.0, 8.0]


class Universe:
    def __init__(self, sx=200, sy=200, population_size=10):
        self.apsolute_time = 0
        self.sx = sx
        self.sy = sy
        self.population_size = population_size
        self.food = pd.DataFrame()
        data = np.fromfunction(Universe.foodShape, [sx, sy])
        self.food = pd.DataFrame(data)
        # print(self.food.head())
        self.population = []
        for _i in range(population_size):
            self.create_brain()
        for _t in range(9):
            self.tick()

    def foodShape(x, y):
        return x * 2 + y * 2

    def create_brain(self):
        c = Code()
        c.initial_generation()
        b = Brain('br1', c)
        b.setPosition(random.randint(0, self.sx), random.randint(0, self.sy))
        self.population.append(b)

    def updateStates(self):
        toRemove = []
        for bi, b in enumerate(self.population):
            # b.prnt()
            b.tick()
            if b.getQuality() <= 0:
                toRemove.append(bi)
            x, y = b.getPosition()
            dx, dy = b.getMove()
            nx = x + dx
            ny = y + dy
            if nx >= self.sx:
                nx = self.sx - 1
            elif nx <= 0:
                nx = 0
            if ny >= self.sy:
                ny = self.sy - 1
            elif ny <= 0:
                ny = 0
            # print(nx, ny, self.food[nx][ny])
            b.addFood(self.food[nx][ny])
            self.food[nx][ny] = 0
            b.setPosition(nx, ny)

        for i in sorted(toRemove, reverse=True):
            del toRemove[i]

    def tick(self):
        self.apsolute_time += 1
        self.updateStates()
        print('Universe ticked:', self.apsolute_time)
        if not self.apsolute_time % 2:
            self.showUniverse()

    def showUniverse(self):
        ax = []
        ay = []
        asize = []
        for b in self.population:
            # print(b)
            x, y = b.getPosition()
            ax.append(x)
            ay.append(y)
            asize.append(b.getQuality())
        sns.heatmap(self.food, annot=False, cbar=False)
        sns.scatterplot(x=ax, y=ay, size=asize, legend=False)  # , annot=False)
        plt.xticks([])
        plt.yticks([])
        plt.tight_layout(pad=0)
        plt.show(block=False)
        plt.savefig('un.' + str(self.apsolute_time) + '.png')


if __name__ == "__main__":
    un = Universe()
