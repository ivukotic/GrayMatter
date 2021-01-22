import random
import threading
import logging
from tkinter import Tk, Label, StringVar, BOTTOM

from brain import Brain
from code import Code
from environment import Environment

from vizualize import platno
import configuration as conf

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )


class Universe:
    def __init__(self, sx=conf.Universe["size_x"], sy=conf.Universe['size_y'], population_size=conf.Universe['population_size']):
        self.apsolute_time = 0
        self.environment = Environment()
        self.sx = sx
        self.sy = sy
        self.population_size = population_size
        self.population = []

        self.start_event = threading.Event()  # these two events start/restart brain threads processing.
        self.continue_event = threading.Event()

        for _i in range(population_size):
            self.create_brain(_i)

        self.init_graphics()

        for _t in range(conf.Universe['max_age']):
            self.tick()

    def __str__(self):
        return '--- ' + str(self.apsolute_time) + ' ---'

    def init_graphics(self):
        self.display = platno()

        self.str_age = StringVar()
        self.age_label = Label(self.display.canvas, textvariable=self.str_age, fg="black")
        self.age_label.pack(side=BOTTOM)

        self.balls = []
        for b in self.population:
            (x, y) = b.getPosition()
            self.balls.append(self.display.canvas.create_oval(x - 2, y - 2, x + 2, y + 2))

        self.display.update()

    def create_brain(self, index):
        c = Code()
        c.initial_generation()
        b = Brain(index, c, self.start_event, self.continue_event)
        b.setPosition([random.randint(0, self.sx), random.randint(0, self.sy)])
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

            (reward, new_position, view) = self.environment.get_response([x, y], [dx, dy])
            # print('pos:', nx, ny, 'direct:', dx, dy, 'reward:', reward, view)
            b.setPosition(new_position)
            b.process_response(reward, view)

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

    def showUniverse(self):
        ax = []
        ay = []
        asize = []
        for bi, b in enumerate(self.population):
            x, y = b.getPosition()
            size = b.getQuality()
            self.display.canvas.coords(self.balls[bi], x - 2, y - 2, x + 2, y + 2)
        self.str_age.set('t: ' + str(self.apsolute_time))
        self.display.update()


if __name__ == "__main__":

    un = Universe()
