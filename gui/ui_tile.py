import tkinter as tk

from PIL import ImageTk

from application.basins_drawer_service import BasinsDrawerService
from domain.image_tile import ImageTile


class UiTile:
    def __init__(self, parent: tk.Canvas, basins_driver: BasinsDrawerService, image_tile: ImageTile, screen_position: (float, float)):
        self.parent = parent
        self.basins_driver = basins_driver
        self.image_tile = image_tile
        self.image_tk = None
        self.screen_position = screen_position

    def update(self):
        image = self.basins_driver.draw(self.image_tile)
        self.image_tk = ImageTk.PhotoImage(image, master=self.parent)
        return self.image_tk

    def clear(self):
        self.image_tk = None
