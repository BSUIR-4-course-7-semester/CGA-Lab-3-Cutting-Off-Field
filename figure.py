from point import Point
from graphics import draw_polygon, get_pixel, calc_intersection_point_of_two_lines
import sdl2.ext
import numpy as np
from math import cos, sin, radians


def move_point(point, dx, dy):
    return Point(point.x + dx, point.y + dy)


def rotate_point(point, angle):
    result_matr = np.matmul(
        [
            point.x,
            point.y
        ], [
            [cos(radians(angle)), -sin(radians(angle))],
            [sin(radians(angle)), cos(radians(angle))]
        ]
    )
    return Point(int(result_matr[0]), int(result_matr[1]))


def make_lines_from_points(points):
    return [[points[i], points[(i + 1) % len(points)]] for i in range(len(points))]

class SquareCuttingOffField:
    def __init__(self, points, color):
        self.points = points
        self.color = color


class Figure:
    def __init__(self, points, color, hidden_color, z_order=None):
        self._init_points = points
        self.points = points
        self.color = color
        self.hidden_color = hidden_color
        self.z_order = z_order
        self._dx = 0
        self._dy = 0
        self._angle = 0

    # def draw(self):
    #
    #     self._points = list(map(lambda p: move_point(p, self._dx, self._dy), self._points))
    #     draw_polygon(self._pixels, self._points, self.color, self._filled)

    def is_point_inside(self, point):
        x_1 = point.x
        # TODO(max) => get from width of window
        x_2 = 640
        y = point.y
        count = 0
        ray = [Point(x_1, y), Point(x_2, y)]

        for line in make_lines_from_points(self.points):
            intersection_point = calc_intersection_point_of_two_lines(ray, line)
            if intersection_point:
                count += 1
        return True if count % 2 == 1 and count != 0 else False

    def move(self, dx, dy):
        self._dx += dx
        self._dy += dy
        self._apply_position()

    def rotate(self, angle):
        self._angle += angle
        self._apply_position()

    def _apply_position(self):
        self.points = list(map(lambda p: rotate_point(p, self._angle), self._init_points))
        self.points = list(map(lambda p: move_point(p, self._dx, self._dy), self.points))
