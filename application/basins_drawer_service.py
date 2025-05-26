from colorsys import hsv_to_rgb

import numpy as np
from PIL import Image

from domain.image_tile import ImageTile
from domain.math_equation import MathEquation


class BasinsDrawerService:
    max_iterations = 100

    saturation_value = 90
    value = 80
    color_by_labels = {
        0: (00, saturation_value, value),
        1: (40, saturation_value, value),
        2: (70, saturation_value, value),
    }

    def __init__(self, roots: list[complex]):
        self.roots = roots
        self.math_equation = MathEquation(roots)

    def draw(self, x: int, y: int, zoom:int = 1, ) -> Image:
        tile = ImageTile(x, y, zoom)
        _, _, labels = self.get_roots_out_of_screen_points(tile)
        return self.create_image(labels, tile)

    def get_roots_out_of_screen_points(self, tile: ImageTile):
        z0s = tile.get_virtual_points_complex()
        return self.math_equation.try_find_root_from(z0s, self.max_iterations)

    def create_image(self, labels, tile: ImageTile):
        screen_points = tile.get_screen_points()
        colors_by_rows = np.column_stack(np.vectorize(self.__get_color_by_cluster_and_iterations)(labels))
        points_infos = np.column_stack((screen_points, colors_by_rows))

        image = Image.new("RGBA", tile.image_size, color='black')
        pixels = image.load()

        for row in points_infos:
            sx = row[0]
            sy = row[1]
            color = row[2], row[3], row[4], row[5] # r, g, b, a
            pixels[sx, sy] = color

        for root in self.math_equation.roots:
            vx, vy = root.real, root.imag
            sx, sy = tile.virtual_to_screen(vx, vy)
            if tile.is_in_image(sx, sy):
                pixels[sx, sy] = (255, 255, 255, 255)

        svx0, svy0 = tile.virtual_to_screen(0, 0)
        if tile.is_in_image(svx0, svy0):
            pixels[svx0, svy0] = (0, 0, 0, 255)

        return image

    def __get_color_by_cluster_and_iterations(self, label: int) -> (int, int, int):
        hue, saturation, value = self.color_by_labels[label]
        hue, saturation, value = hue / 100., saturation / 100., value / 100.
        r, g, b = hsv_to_rgb(hue, saturation, value)
        return int(r * 255), int(g * 255), int(b * 255), 255
