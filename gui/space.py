from tkinter import Frame, Canvas, ALL
from typing import List

from PIL import ImageTk

from application.basins_drawer_service import BasinsDrawerService
from domain.image_tile import ImageTile


class MovementCalculator:
    def __init__(self):
        self.x0 = None
        self.y0 = None

    def calculate(self, x, y):
        dx, dy = 0, 0
        if self.x0 is not None:
            dx = x - self.x0
        if self.y0 is not None:
            dy = y - self.y0
        self.x0, self.y0 = x, y
        return dx, dy

    def reset(self):
        self.x0 = None
        self.y0 = None


class Space(Frame):
    TILES_TAG = "basins_tiles"

    def __init__(self, parent, drawer : BasinsDrawerService, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.movement_calculator = MovementCalculator()
        self.x = 0
        self.y = 0
        self.zoom = 1
        self.temp_tile = ImageTile(self.x, self.y, self.zoom, drawer)

        self.images: List[ImageTk.PhotoImage] = []
        self.canvas = Canvas(self, width=parent.winfo_width(), height=parent.winfo_width())
        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<B1-ButtonRelease>', lambda _: self.movement_calculator.reset())
        self.canvas.bind('<MouseWheel>', self.do_zoom)
        self.canvas.pack(side="top", fill="both", expand=True)

    def do_zoom(self, event) -> object:
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.zoom *= factor
        self.canvas.scale(ALL, x, y, factor, factor)

    def drag(self, event) -> object:
        dx, dy = self.movement_calculator.calculate(event.x, event.y)
        self.move(dx, dy)

    def move(self, x, y):
        # self.canvas.itemconfig(img, state="hidden")
        self.x = x
        self.y = y
        self.canvas.move(ALL, x, y)

    def move_left(self):
        self.move(-10, 0)

    def move_right(self):
        self.move(10, 0)

    def clear_elements(self):
        self.images = []

    def update(self):
        image = self.temp_tile.draw()
        image_tk = ImageTk.PhotoImage(image, master=self)
        self.canvas.create_image(self.winfo_width() / 2, self.winfo_height() / 2, image=image_tk, tag=Space.TILES_TAG)
        self.images.append(image_tk)
