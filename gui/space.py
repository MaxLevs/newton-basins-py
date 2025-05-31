from tkinter import Frame, Canvas, ALL
from typing import List
import math

from application.basins_drawer_service import BasinsDrawerService
from domain.image_tile import ImageTile
from gui.ui_tile import UiTile


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

    def __init__(self, parent, drawer: BasinsDrawerService, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.movement_calculator = MovementCalculator()
        self.basins_drawer = drawer

        self.x = 0
        self.y = 0
        self.zoom = 1

        self.tiles: List[UiTile] = []

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
        self.x = x
        self.y = y
        self.canvas.move(ALL, x, y)

    def move_left(self):
        self.move(-10, 0)

    def move_right(self):
        self.move(10, 0)

    def temp_generate_position_factions(self, n: int):
        for i in range(n):
            yield i
            if i != 0:
                yield -i

    def temp_create_tiles(self):
        screen_x = self.winfo_width()
        screen_y = self.winfo_height()
        gen_x = list(self.temp_generate_position_factions(math.ceil(screen_x / ImageTile.image_x_max)))
        gen_y = list(self.temp_generate_position_factions(math.ceil(screen_y / ImageTile.image_y_max)))
        center_x = screen_x / 2
        center_y = screen_y / 2
        coords = [(center_x + fraction_x * ImageTile.image_x_max, center_y + fraction_y * ImageTile.image_y_max) for fraction_x in gen_x for fraction_y in gen_y]
        for x, y in coords:
            image_tile = ImageTile((x - center_y) / ImageTile.basic_zoom, -(y - center_y) / ImageTile.basic_zoom, 1, self.basins_drawer)
            self.tiles.append(UiTile(self.canvas, image_tile, (x, y)))

    def clear_elements(self):
        for tile in self.tiles:
            tile.clear()

    def update(self):
        if not self.tiles:
            self.temp_create_tiles()

        for tile in self.tiles:
            image_tk = tile.update()
            self.canvas.create_image(tile.screen_position[0], tile.screen_position[1], image=image_tk, tag=Space.TILES_TAG)
