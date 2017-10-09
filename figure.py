from graphics import draw_polygon, get_pixel, calc_intersection_point_of_two_lines, Point
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
    def __init__(self, top, right, bottom, left, color):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        self.points = [
            Point(left, top),
            Point(right, top),
            Point(right, bottom),
            Point(left, bottom)
        ]
        self.color = color

    def is_point_hidden(self, point):
        if self.left <= point.x <= self.right and self.top <= point.y <= self.bottom:
            return False
        return True

    def get_cohen_sutherland_code_for_point(self, point):
        res = 0
        if point.x <= self.left:
            res |= 8
        elif point.x >= self.right:
            res |= 4
        if point.y <= self.top:
            res |= 1
        elif point.y >= self.bottom:
            res |= 2
        return res


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

    def is_point_inside(self, point):
        x_1 = point.x
        # TODO(max) => get from width of window
        x_2 = 640
        y = point.y
        count = 0
        ray = [Point(x_1, y), Point(x_2, y)]

        lines_from_points = make_lines_from_points(self.points)
        for line in lines_from_points:
            intersection_point, _ = calc_intersection_point_of_two_lines(ray, line)
            if intersection_point:
                count += 1

        return True if count % 2 == 1 else False

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
