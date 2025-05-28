import tkinter as tk

from PIL import ImageTk

from domain.image_tile import ImageTile


class UiTile:
    def __init__(self, parent: tk.Canvas, image_tile: ImageTile, screen_position: (float, float)):
        self.parent = parent
        self.image_tile = image_tile
        self.image_tk = None
        self.screen_position = screen_position

    def update(self):
        image = self.image_tile.draw()
        self.image_tk = ImageTk.PhotoImage(image, master=self.parent)
        return self.image_tk

    def clear(self):
        self.image_tk = None
