from colorsys import hsv_to_rgb

class RootColor:
    def __init__(self, hue: int, saturation: int, value: int):
        self.__ensure_valid_value(hue, "hue")
        self.__ensure_valid_value(saturation, "saturation")
        self.__ensure_valid_value(value, "value")

        self.hue = hue
        self.saturation = saturation
        self.value = value

    def get_rgba(self):
        r, g, b = self.get_rgb()
        return r,g,b, 255

    def get_rgb(self):
        r, g, b = hsv_to_rgb(self.hue / 100., self.saturation / 100., self.value / 100.)
        return int(r * 255), int(g * 255), int(b * 255)

    def __ensure_valid_value(self, param: int, param_name: str):
        if not self.__is_in_valid_range(param):
            raise ValueError(f'Color param {param_name} must be between 0 and 100')

    # noinspection PyMethodMayBeStatic
    def __is_in_valid_range(self, param) -> bool:
            return 0 <= param <= 100
