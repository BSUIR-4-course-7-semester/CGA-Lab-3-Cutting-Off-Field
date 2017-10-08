from figure import make_lines_from_points
from graphics import draw_line, draw_polygon, calc_intersection_point_of_two_lines


class Drawer:
    def __init__(self, pixels, cutting_off_field, figures):
        self._cutting_off_field = cutting_off_field
        self._figures = figures
        self._pixels = pixels

    def draw(self):
        draw_polygon(self._pixels, self._cutting_off_field.points, self._cutting_off_field.color)

        # figures = {i: {'lines': make_lines_from_points(self._figures[i].points),
        #  'color': self._figures[i].color, 'hidden_color': self._figures[i].hidden_color}
        #  for i in range(len(self._figures))}

        fig_a = self._figures[0]
        fig_b = self._figures[1]

        lines_a = make_lines_from_points(fig_a.points)
        lines_b = make_lines_from_points(fig_b.points)

        points_a = fig_a.points
        points_b = []

        for line_b in lines_b:
            intersection_points = []
            mu_vector = []
            for line_a in lines_a:
                intersection_point, mu = calc_intersection_point_of_two_lines(line_a, line_b)
                if intersection_point is not None:
                    intersection_points.append(intersection_point)
                    mu_vector.append(mu)

            pack = list(zip(intersection_points, mu_vector))
            pack.sort(key=lambda a: a[1])
            intersection_points = list(map(lambda a: a[0], pack))

            points_b.append(line_b[0])
            points_b.extend(intersection_points)
            points_b.append(line_b[1])

        draw_polygon(self._pixels, points_a, fig_a.color)
        draw_polygon(self._pixels, points_b, fig_b.color)

        # for figure in self._figures:
        #     self._draw_polygon_with_cutting_off(figure)

    def _draw_polygon_with_cutting_off(self, polygon):
        draw_polygon(self._pixels, polygon.points, polygon.color)