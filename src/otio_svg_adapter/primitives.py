import random

random_colors_used = []


class Color:
    def __init__(self, r=0.0, g=0.0, b=0.0, a=255.0):
        self.value = (r, g, b, a)

    def __getitem__(self, item):
        return self.value[item]

    @staticmethod
    def random_color():
        color = Color.__generate_new_color()
        random_colors_used.append(color)
        return color

    @staticmethod
    def __generate_new_color():
        max_distance = None
        best_color = None
        for _ in range(100):
            color = Color.__get_random_color()
            if len(random_colors_used) == 0:
                return color
            best_distance = min(
                [Color.__color_distance(color, c) for c in random_colors_used]
            )
            if not max_distance or best_distance > max_distance:
                max_distance = best_distance
                best_color = color
        return best_color

    @staticmethod
    def __get_random_color():
        return Color(random.random(), random.random(), random.random(), 1.0)

    @staticmethod
    def __color_distance(c1, c2):
        return sum([abs(x[0] - x[1]) for x in zip(c1.value, c2.value)])

    @property
    def r(self):
        return self.value[0]

    @property
    def g(self):
        return self.value[1]

    @property
    def b(self):
        return self.value[2]

    @property
    def a(self):
        return self.value[3]

    def svg_color(self):
        return "rgb({:.8f},{:.8f},{:.8f})".format(
            self.r * 255.0, self.g * 255.0, self.b * 255.0
        )


COLORS = {
    "transparent": Color(0, 0, 0, 0),
    "black": Color(0.0, 0.0, 0.0, 1.0),
    "white": Color(1.0, 1.0, 1.0, 1.0),
    "transluscent_white": Color(1.0, 1.0, 1.0, 0.7),
    "purple": Color(0.5, 0.0, 0.5, 1.0),
    "light_blue": Color(0.529, 0.808, 0.922, 1.0),
    "blue": Color(0.0, 0.0, 1.0, 1.0),
    "dark_blue": Color(0.0, 0.0, 0.54, 1.0),
    "green": Color(0.0, 0.5, 0.0, 1.0),
    "dark_green": Color(0.0, 0.39, 0.0, 1.0),
    "yellow": Color(1.0, 1.0, 0.0, 1.0),
    "gold": Color(1.0, 0.84, 0.0, 1.0),
    "orange": Color(1.0, 0.647, 0.0, 1.0),
    "red": Color(1.0, 0.0, 0.0, 1.0),
    "dark_red": Color(0.54, 0.0, 0.0, 1.0),
    "brown": Color(0.54, 0.27, 0.1, 1.0),
    "pink": Color(1.0, 0.75, 0.79, 1.0),
    "gray": Color(0.5, 0.5, 0.5, 1.0),
    "dark_gray": Color(0.66, 0.66, 0.66, 1.0),
    "dark_gray_transluscent": Color(0.66, 0.66, 0.66, 0.7843),
}


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def svg_point_string(self):
        return f"{self.x:.8f},{self.y:.8f}"


class Rect:
    origin = Point(0, 0)
    width = 0.0
    height = 0.0

    def __init__(self, origin=Point(0, 0), width=0.0, height=0.0):
        self.origin = origin
        self.width = width
        self.height = height

    def normalized(self):
        normalized_origin = Point(
            self.origin.x + (self.width if self.width < 0 else 0),
            self.origin.y + (self.height if self.height < 0 else 0),
        )
        normalized_width = abs(self.width)
        normalized_height = abs(self.height)
        return Rect(normalized_origin, normalized_width, normalized_height)

    def min_x(self):
        return self.normalized().origin.x

    def min_y(self):
        return self.normalized().origin.y

    def mid_x(self):
        return self.origin.x + (self.width * 0.5)

    def mid_y(self):
        return self.origin.y + (self.height * 0.5)

    def max_x(self):
        norm = self.normalized()
        return norm.origin.x + norm.width

    def max_y(self):
        norm = self.normalized()
        return norm.origin.y + norm.height

    def contract(self, distance):
        self.origin.x += distance
        self.origin.y += distance
        self.width -= 2.0 * distance
        self.height -= 2.0 * distance


def convert_point_to_svg_coordinates(point, image_height):
    y = image_height - point.y
    return Point(point.x, y)


def convert_rect_to_svg_coordinates(rect, image_height):
    """Convert to SVG coordinate system (0,0 at top-left)"""
    normalized_rect = rect.normalized()
    normalized_rect.origin = convert_point_to_svg_coordinates(
        normalized_rect.origin, image_height
    )
    normalized_rect.height *= -1
    return normalized_rect.normalized()
