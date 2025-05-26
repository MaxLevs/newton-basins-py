import numpy as np

class ImageTile:
    image_x_max = 256
    image_y_max = 256
    image_size = (image_x_max, image_y_max)

    vx0, vy0 = image_x_max / 2., image_y_max / 2.
    zoom = min(image_x_max, image_y_max) / 10.  # basic value

    def __init__(self, x: int, y: int, zoom: float):
        self.eye_vx = x  # change to converting tile coords to virtual coords
        self.eye_vy = y
        self.zoom *= zoom  # basic zoom multiplied by eye_zoom

    def is_in_image(self, x, y):
        return (0 <= x < self.image_size[0] - 1) and (0 <= y < self.image_size[1] - 1)

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
        image_screen_points_generator = [(sx, sy) for sx in x_range for sy in y_range]
        return np.array(image_screen_points_generator)

    def get_virtual_points(self):
        sps = self.get_screen_points()
        sps_x, sps_y = sps[:, 0], sps[:, 1]
        # noinspection PyTypeChecker
        vps_x, vps_y = self.screen_to_virtual(sps_x, sps_y)
        return np.column_stack((vps_x, vps_y))
