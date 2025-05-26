from PIL import Image
from sympy import symbols, diff, lambdify
from math import prod
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import scipy.optimize as sopt


class DataFields:
    screen_x = 'Screen X'
    screen_y = 'Screen Y'
    root_virtual_x = 'Root Virtual X'
    root_virtual_y = 'Root Virtual Y'
    converged = 'Converged'
    label = 'Label'
    color = 'Color'


class ImageTile:
    image_x_max = 256
    image_y_max = 256
    image_size = (image_x_max, image_y_max)

    vx0, vy0 = image_x_max / 2., image_y_max / 2.
    zoom = min(image_x_max, image_y_max) / 10. # basic value

    def __init__(self, x: int, y: int, zoom: float):
        self.eye_vx = x # change to converting tile coords to virtual coords
        self.eye_vy = y
        self.zoom *= zoom # basic zoom multiplied by eye_zoom

    def virtual_to_screen(self, vx: float, vy: float) -> (int, int):
        sx = int(round(self.vx0 - (self.eye_vx - vx) * self.zoom))
        sy = int(round(self.vy0 - (vy - self.eye_vy) * self.zoom))
        return sx, sy

    def screen_to_virtual(self, sx: int, sy: int) -> (float, float):
        vx = (sx - self.vx0) / self.zoom + self.eye_vx
        vy = (self.vy0 - sy) / self.zoom + self.eye_vy
        return vx, vy

    def get_screen_points(self):
        x_range = range(self.image_size[0])
        y_range = range(self.image_size[1])
        image_screen_points_generator = ((sx, sy) for sx in x_range for sy in y_range)
        return np.array(image_screen_points_generator)

    def get_virtual_points(self):
        sps = self.get_screen_points()
        spsx, spsy = sps[:, 0], sps[:, 1]
        # noinspection PyTypeChecker
        vpsx, vpsy = self.screen_to_virtual(spsx, spsy)
        return np.transpose(np.concatenate((vpsx, vpsy), axis=0))


class BasinsDrawerService:
    target_roots = [
        1.2 - 4*1j,
        3 + 2.4*1j,
        -1.2 - 1.4*1j
    ]
    max_iterations = 100

    saturation_value = 90
    value = 80
    color_by_labels = {
        0: (00, saturation_value, value),
        1: (40, saturation_value, value),
        2: (70, saturation_value, value),
    }

    def draw(self, x, y, zoom = 1) -> Image:
        tile = ImageTile(x, y, zoom)

        f, df = self.create_function()
        approximate_roots = self.get_roots_out_of_screen_points(f, df, tile.get_virtual_points())
        approximate_roots = self.clusterize_approximate_roots(approximate_roots)

        image = Image.new("RGBA", tile.image_size, color='black')
        return image

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
            DataFields.screen_x: spsx,
            DataFields.screen_y: spsy,
            DataFields.root_virtual_x: np.vectorize(lambda z: z.real)(res.root),
            DataFields.root_virtual_y: np.vectorize(lambda z: z.imag)(res.root),
            DataFields.converged: res.converged,
        })

    def clusterize_approximate_roots(self, approximate_roots: pd.DataFrame):
        model = KMeans(n_clusters=len(self.target_roots), n_init=8, random_state=42)
        clusters = model.fit_predict(approximate_roots[[DataFields.root_virtual_x, DataFields.root_virtual_y]].values)
        return pd.concat([approximate_roots, pd.DataFrame(clusters, columns=[DataFields.label])], axis=1)

    def create_image(self, approximate_roots: pd.DataFrame, ):


