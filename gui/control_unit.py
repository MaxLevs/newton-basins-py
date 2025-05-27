from tkinter import Frame


class ControlUnit(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    # noinspection PyUnresolvedReferences
    def place(self, func):
        func(self)
        return self
