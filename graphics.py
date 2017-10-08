from random import randint

import sdl2.ext
from sdl2 import SDL_Point


class Point(SDL_Point):
    def __init__(self, a, b):
        super(Point, self).__init__(a, b)
        self.visibility = None

    def __add__(self, value):
        return Point(self.x + value.x, self.y + value.y)


def draw_polygon(pixels, points, color):
    point_count = len(points)
    for i in range(point_count):
        draw_line(pixels, points[i], points[(i + 1) % point_count], color)


def normalize_point(point):
    return Point(
        639 if point.x >= 640 else 0 if point.x < 0 else point.x,
        479 if point.y >= 480 else 0 if point.y < 0 else point.y,
    )


def get_pixel(pixels, point):
    point = normalize_point(point)
    return pixels[point.y][point.x]


def put_pixel(pixels, point, color):
    point = normalize_point(point)
    pixels[point.y][point.x] = color


def draw_line(pixels, point_a, point_b, color):
    dx = abs(point_a.x - point_b.x)
    dy = abs(point_a.y - point_b.y)

    sx = 1 if point_b.x >= point_a.x else -1
    sy = 1 if point_b.y >= point_a.y else -1

    if dy <= dx:
        d = dy * 2 - dx
        d1 = dy * 2
        d2 = (dy - dx) * 2

        put_pixel(pixels, point_a, color)
        x = point_a.x + sx
        y = point_a.y
        for i in range(1, dx + 1):
            if d > 0:
                d += d2
                y += sy
            else:
                d += d1

            put_pixel(pixels, Point(x, y), color)
            x += sx
    else:
        d = dx * 2 - dy
        d1 = dx * 2
        d2 = (dx - dy) * 2

        put_pixel(pixels, point_a, color)
        x = point_a.x
        y = point_a.y + sy
        for i in range(1, dy + 1):
            if d > 0:
                d += d2
                x += sx
            else:
                d += d1

            put_pixel(pixels, Point(x, y), color)
            y += sy


def draw_circle(pixels, point, radius, color):
    x = 0
    y = radius
    delta = 1 - 2 * radius
    err = 0

    while y >= 0:
        put_pixel(pixels, point + SDL_Point(x, y), color)
        put_pixel(pixels, point + SDL_Point(x, -y), color)
        put_pixel(pixels, point + SDL_Point(-x, y), color)
        put_pixel(pixels, point + SDL_Point(-x, -y), color)
        err = 2 * (delta + y) - 1

        if delta < 0 and err <= 0:
            x += 1
            delta += 2 * x + 1
            continue
        else:
            err = 2 * (delta - x) - 1
            if delta > 0 and err > 0:
                y -= 1
                delta += 1 - 2 * y
            else:
                x += 1
                delta += 2 * (x - y)
                y -= 1


def is_point_on_lines(point, lines):
    for line in lines:
        a = line[1].x - line[0].x

        if a == 0:
            a = line[1].y - line[0].y
            # TODO(max) => handle if a == 0
            mu = (point.y - line[0].y) / a
        else:
            mu = (point.x - line[0].x) / a

        if mu < 0 or mu > 1:
            return None
    return mu


def calc_intersection_point_of_two_lines(line_a, line_b):
    x_1 = line_a[0].x
    y_1 = line_a[0].y
    x_2 = line_a[1].x
    y_2 = line_a[1].y
    x_3 = line_b[0].x
    y_3 = line_b[0].y
    x_4 = line_b[1].x
    y_4 = line_b[1].y

    denominator = (x_1 - x_2) * (y_3 - y_4) - (y_1 - y_2) * (x_3 - x_4)
    if denominator == 0:
        return None, None

    a = x_1 * y_2 - y_1 * x_2
    b = x_3 * y_4 - y_3 * x_4

    x_numerator = a * (x_3 - x_4) - (x_1 - x_2) * b
    x = x_numerator / denominator
    y_numerator = a * (y_3 - y_4) - (y_1 - y_2) * b
    y = y_numerator / denominator

    point = Point(round(x), round(y))

    mu = is_point_on_lines(point, [line_a, line_b])
    return (point, mu) if mu is not None else (None, None)

