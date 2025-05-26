from colorsys import hsv_to_rgb
from math import prod

import numpy as np
import pandas as pd
import scipy.optimize as sopt
from PIL import Image
from sklearn.cluster import KMeans
from sympy import symbols, diff, lambdify

from application.constants import DataFields
from application.image_tile import ImageTile
from application.utils.pandas_helper import PandasHelper


class BasinsDrawerService:
    target_roots = [
        complex(1.2, -4),
        complex(3, 2.4),
        complex(-1.2, - 1.4),
    ]
    max_iterations = 100

    saturation_value = 90
    value = 80
    color_by_labels = {
        0: (00, saturation_value, value),
        1: (40, saturation_value, value),
        2: (70, saturation_value, value),
    }

    def draw(self, x, y, zoom=1) -> Image:
        tile = ImageTile(x, y, zoom)

        f, df = self.create_function()
        approximate_roots = self.get_roots_out_of_screen_points(f, df, tile.get_virtual_points())

        return self.create_image(approximate_roots, tile)

    def create_function(self):
        variable = symbols('z')
        func_f = prod(map(lambda root: variable - root, self.target_roots))
        func_df = diff(func_f, variable)
        return lambdify(variable, func_f, 'numpy'), lambdify(variable, func_df, 'numpy')

    # noinspection PyUnresolvedReferences
    def get_roots_out_of_screen_points(self, f, df, starting_points):
        vps = starting_points[:, 0] + starting_points[:, 1] * 1j
        res = sopt.newton(f, fprime=df, x0=vps, maxiter=self.max_iterations, full_output=True)
        return pd.DataFrame.from_dict({
            DataFields.root_virtual_x: np.vectorize(lambda z: z.real)(res.root),
            DataFields.root_virtual_y: np.vectorize(lambda z: z.imag)(res.root),
            DataFields.converged: res.converged,
        })

    def clusterize_approximate_roots(self, approximate_roots: pd.DataFrame):
        model = KMeans(n_clusters=len(self.target_roots), n_init=8, random_state=42)
        return model.fit_predict(approximate_roots[[DataFields.root_virtual_x, DataFields.root_virtual_y]].values)

    def create_image(self, approximate_roots: pd.DataFrame, tile: ImageTile):
        approximate_roots = PandasHelper.append_to_dataframe(approximate_roots, tile.get_screen_points(),
                                                             [DataFields.screen_x, DataFields.screen_y])

        labels = self.clusterize_approximate_roots(approximate_roots)
        approximate_roots = PandasHelper.append_to_dataframe(approximate_roots, labels, [DataFields.label])

        colors_by_rows = np.column_stack(np.vectorize(self.get_color_by_cluster_and_iterations)(labels))
        approximate_roots = PandasHelper.append_to_dataframe(approximate_roots, colors_by_rows,
                                                             [DataFields.color_r, DataFields.color_g,
                                                              DataFields.color_b, DataFields.color_a])

        image = Image.new("RGBA", tile.image_size, color='black')
        pixels = image.load()

        for row in approximate_roots.itertuples():
            # sx = row[datafields.screen_x]
            # sy = row[datafields.screen_y]
            # color = row[datafields.color_r], row[datafields.color_g], row[datafields.color_b], row[datafields.color_a]
            sx = row[4]
            sy = row[5]
            color = row[7], row[8], row[9], row[10]
            pixels[sx, sy] = color

        for root in self.target_roots:
            vx, vy = root.real, root.imag
            sx, sy = tile.virtual_to_screen(vx, vy)
            print(vx, vy, sx, sy)
            if tile.is_in_image(sx, sy):
                pixels[sx, sy] = (255, 255, 255, 255)

        svx0, svy0 = tile.virtual_to_screen(0, 0)
        if tile.is_in_image(svx0, svy0):
            pixels[svx0, svy0] = (0, 0, 0, 255)

        return image

    def get_color_by_cluster_and_iterations(self, label: int) -> (int, int, int):
        hue, saturation, value = self.color_by_labels[label]
        hue, saturation, value = hue / 100., saturation / 100., value / 100.
        r, g, b = hsv_to_rgb(hue, saturation, value)
        return int(r * 255), int(g * 255), int(b * 255), 255
