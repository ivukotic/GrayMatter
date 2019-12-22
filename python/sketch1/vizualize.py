from tkinter import Tk, Canvas
from brain import Brain

class Display:
    def __init__(self, obj):
        self.obj = obj
        self.tk = Tk()
        self.tk.title(self.obj.name)
        self.canvas = Canvas(self.tk, width=300, height=300)
        self.canvas.pack(fill="both", expand="yes")
        self.canvas.pack_propagate(0)
        self.show()

    def show(self):  # not used
        if isinstance(self.obj, Brain):
            print('Drawing brain')
            self.canvas.create_oval(100, 100, 200, 200)
            self.tk.update()
