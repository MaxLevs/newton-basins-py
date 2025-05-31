from PIL import Image

import common.utils as utils
from application.equation_solver import *
from domain.image_tile import *
from domain.math_equation import *
from domain.root_color import *


class BasinsDrawerService:
    max_iterations = 100

    color_by_labels = {
        0: RootColor(00, 75, 80),
        1: RootColor(40, 85, 80),
        2: RootColor(70, 90, 80),
    }

    def __init__(self, roots: list[complex]):
        self.roots = roots
        self.math_equation = PolynomialMathEquation(roots)
        self.equation_solver = EquationSolver(self.max_iterations)
        self.__get_color_by_cluster_and_iterations_vector = np.vectorize(self.__get_color_by_cluster_and_iterations)

    # @utils.timing
    def draw(self, tile: ImageTile) -> Image:
        labels = self.get_roots_out_of_screen_points(tile)
        return self.create_image(labels, tile)

    # @utils.timing
    def get_roots_out_of_screen_points(self, tile: ImageTile):
        z0s = tile.get_virtual_points_complex()
        _, labels = self.equation_solver.try_find_roots(self.math_equation, z0s)
        return labels

    # @utils.timing
    def create_image(self, labels, tile: ImageTile):
        colors_by_rows = np.column_stack(self.__get_color_by_cluster_and_iterations_vector(labels))
        colors_by_rows = colors_by_rows.astype(np.uint8).reshape((tile.image_x_max, tile.image_y_max, 3))
        colors_by_rows = np.moveaxis(colors_by_rows, 1, 0)
        image = Image.fromarray(colors_by_rows, 'RGB')
        return image

    def __get_color_by_cluster_and_iterations(self, label: int) -> (int, int, int):
        color = self.color_by_labels[label]
        return color.get_rgb()
