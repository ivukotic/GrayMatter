import random
import threading
import logging
from tkinter import Tk, Canvas, Label, StringVar, BOTTOM

import numpy as np
import pandas as pd
from brain import Brain
from code import Code

from vizualize import Display
import configuration as conf

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )


class Universe:
    def __init__(self, sx=conf.Universe["size_x"], sy=conf.Universe['size_y'], population_size=conf.Universe['population_size']):
        self.apsolute_time = 0
        # these two events start/restart brain threads processing.
        self.start_event = threading.Event()
        self.continue_event = threading.Event()
        self.sx = sx
        self.sy = sy
        self.food = pd.DataFrame(np.fromfunction(lambda x, y: x * 2 + y * 2, [self.sx, self.sy]))
        self.population_size = population_size
        self.population = []
        for _i in range(population_size):
            self.create_brain(_i)

        self.init_graphics()

        for _t in range(conf.Universe['max_age']):
            self.tick()

    def __str__(self):
        return '--- ' + str(self.apsolute_time) + ' ---'

    def init_graphics(self, scale=3):
        self.canvas = Canvas(tk, width=self.sx * scale, height=self.sy * scale)
        self.canvas.pack(fill="both", expand="yes")
        self.canvas.pack_propagate(0)

        self.str_age = StringVar()
        self.age_label = Label(self.canvas, textvariable=self.str_age, fg="black")
        self.age_label.pack(side=BOTTOM)

        self.balls = []
        for b in self.population:
            (x, y) = b.getPosition()
            self.balls.append(self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2))

        tk.update()

    def create_brain(self, index):
        c = Code()
        c.initial_generation()
        b = Brain(index, c, self.start_event, self.continue_event)
        b.setPosition(random.randint(0, self.sx), random.randint(0, self.sy))
        self.population.append(b)
        b.start()

    def updateStates(self):
        # wait until all brains delivered tick result.
        while True:
            if len(Brain.actions) == self.population_size:
                break
        Brain.actions.clear()

        # logging.debug('do actual collection')

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

        if conf.viz:
            self.showUniverse()

        self.print_out()
        if conf.special_show_at == self.apsolute_time:
            self.print_detailed()

    def print_out(self):
        _ind, level = conf.print_opt['Universe']
        if level == 0:
            return
        print(self)
        if level > 1:
            print('population size:', len(self.population))

    def print_detailed(self):
        self.population[0].print_detailed()
        Display(self.population[0])

    def showUniverse(self):
        ax = []
        ay = []
        asize = []
        for bi, b in enumerate(self.population):
            x, y = b.getPosition()
            x *= 3
            y *= 3
            size = b.getQuality()
            self.canvas.coords(self.balls[bi], x - 2, y - 2, x + 2, y + 2)
        self.str_age.set('t: ' + str(self.apsolute_time))
        tk.update()


if __name__ == "__main__":

    tk = Tk()
    tk.title("Universe")
    # tk.mainloop()
    un = Universe()
