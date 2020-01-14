from tkinter import Tk, Canvas


class Display:

    def __init__(self, title, width, height):
        self.tk = Tk()
        self.tk.title(title)
        self.canvas = Canvas(self.tk, width=width, height=height)
        self.canvas.pack(fill="both", expand="yes")
        self.canvas.pack_propagate(0)
        self.update()

    def update(self):
        self.tk.update()


_platno = None


def platno(title='not defined', width=300, height=300):
    global _platno
    if _platno is None:
        _platno = Display(title, width, height)
    return _platno
