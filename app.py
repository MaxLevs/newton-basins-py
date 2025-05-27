import tkinter as tk
from typing import List

from PIL import ImageTk

from application.basins_drawer_service import BasinsDrawerService


class ControlUnit(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

    # noinspection PyUnresolvedReferences
    def place(self, func):
        func(self)
        return self


class Space(tk.Frame):
    TILES_TAG = "basins_tiles"

    def __init__(self, parent, drawer, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.x0 = None
        self.y0 = None
        self.drawer = drawer

        self.tk_images : List[ImageTk.PhotoImage] = []
        self.canvas = tk.Canvas(self, width=parent.winfo_width(), height=parent.winfo_width())
        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<B1-ButtonRelease>', self.reset_drag)
        self.canvas.bind('<MouseWheel>', self.zoom)
        self.canvas.pack(side="top", fill="both", expand=True)


    def zoom(self, event) -> object:
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.canvas.scale(tk.ALL, x, y, factor, factor)

    def drag(self, event) -> object:
        dx, dy = 0, 0
        if self.x0 is not None:
            dx = event.x - self.x0
        if self.y0 is not None:
            dy = event.y - self.y0
        self.x0, self.y0 = event.x, event.y
        self.move(dx, dy)

    def reset_drag(self, event) -> object:
        self.x0, self.y0 = None, None

    def move(self, x, y):
        # self.canvas.itemconfig(img, state="hidden")
        self.canvas.move(tk.ALL, x, y)

    def move_left(self):
        self.move(-10, 0)

    def move_right(self):
        self.move(10, 0)

    def clear_elements(self):
        self.tk_images = []

    def draw(self):
        image = self.drawer.draw(0, 0, 1)
        tk_image = ImageTk.PhotoImage(image, master=self)
        self.canvas.create_image(image.size[0], image.size[1], image=tk_image, tag=Space.TILES_TAG)
        self.tk_images.append(tk_image)


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.roots = [complex(1.2, -4), complex(3, 2.4), complex(-1.2, - 1.4), ]
        self.drawer = BasinsDrawerService(self.roots)
        space = Space(self, self.drawer)

        cu = ControlUnit(self, *args, **kwargs)
        cu.place(lambda itself: tk.Button(itself, text='Move Left', command=space.move_left).pack(side="left"))
        cu.place(lambda itself: tk.Button(itself, text='Calculate', command=space.draw).pack(side="left"))
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
