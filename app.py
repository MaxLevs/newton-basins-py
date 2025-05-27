import tkinter as tk

from gui.control_unit import *
from gui.space import *


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.roots = [complex(1.2, -4), complex(3, 2.4), complex(-1.2, - 1.4), ]
        self.drawer = BasinsDrawerService(self.roots)
        space = Space(self, self.drawer)

        cu = ControlUnit(self, *args, **kwargs)
        cu.place(lambda itself: tk.Button(itself, text='Move Left', command=space.move_left).pack(side="left"))
        cu.place(lambda itself: tk.Button(itself, text='Calculate', command=space.update).pack(side="left"))
        cu.place(lambda itself: tk.Button(itself, text='Move Right', command=space.move_right).pack(side="left"))
        cu.place(lambda itself: tk.Button(itself, text='Clear All', command=space.clear_elements).pack(side="left"))
        cu.pack(side="top")

        space.pack(side="top", fill="both", expand=True)


if __name__ == "__main__":
    tk_root = tk.Tk()
    tk_root.title("Newton's basins")
    tk_root.geometry(f'512x512')
    app = MainApplication(tk_root)
    app.pack(side="top", fill="both", expand=True)

    tk_root.mainloop()
