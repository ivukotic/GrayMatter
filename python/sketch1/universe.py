import random
import threading

import numpy as np
import pandas as pd
from brain import Brain
from code import Code

from tkinter import *


class Universe:
    def __init__(self, sx=200, sy=200, population_size=10):
        self.apsolute_time = 0
        self.start_event = threading.Event()
        self.continue_event = threading.Event()
        self.sx = sx
        self.sy = sy
        self.food = pd.DataFrame(np.fromfunction(lambda x, y: x * 2 + y * 2, [self.sx, self.sy]))
        self.population_size = population_size
        self.population = []
        for _i in range(population_size):
            self.create_brain('Br_' + str(_i))

        self.init_graphics()

        for _t in range(9):
            self.tick()

    def init_graphics(self):
        self.canvas = Canvas(tk, width=self.sx, height=self.sy)
        self.canvas.pack()
        self.balls = []
        for b in self.population:
            (x, y) = b.getPosition()
            self.balls.append(self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2))
        tk.update()

    def create_brain(self, name):
        c = Code()
        c.initial_generation()
        b = Brain(name, c, self.start_event, self.continue_event)
        b.setPosition(random.randint(0, self.sx), random.randint(0, self.sy))
        self.population.append(b)
        b.start()

    def updateStates(self):
        while True:
            if len(Brain.actions) == self.population_size:
                break
        Brain.actions.clear()
        print('do actual collection')
        toRemove = []
        for bi, b in enumerate(self.population):
            # b.prnt()
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

        self.continue_event.clear()
        self.start_event.set()
        self.apsolute_time += 1
        self.updateStates()
        self.start_event.clear()
        self.continue_event.set()
        print('Universe ticked:', self.apsolute_time)
        if not self.apsolute_time % 2:
            self.showUniverse()

    def showUniverse(self):
        ax = []
        ay = []
        asize = []
        for bi, b in enumerate(self.population):
            x, y = b.getPosition()
            size = b.getQuality()
            self.canvas.coords(self.balls[bi], x - 2, y - 2, x + 2, y + 2)
        tk.update()


if __name__ == "__main__":

    tk = Tk()
    tk.title("Universe")
    # tk.mainloop()
    un = Universe()
