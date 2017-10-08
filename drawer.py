from figure import make_lines_from_points
from graphics import draw_line, draw_polygon, calc_intersection_point_of_two_lines

VISIBLE = 'visible'
HIDDEN = 'hidden'
TRANSITIVE = 'transitive'

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
        lines_cutting_off = make_lines_from_points(self._cutting_off_field.points)

        points_a = []
        points_b = []

        for line_b in lines_b:
            intersection_points = []
            mu_vector = []
            for line in lines_a + lines_cutting_off:
                intersection_point, mu = calc_intersection_point_of_two_lines(line, line_b)
                if intersection_point is not None:
                    intersection_points.append(intersection_point)
                    mu_vector.append(mu)
                    intersection_point.visibility = TRANSITIVE

            pack = list(zip(intersection_points, mu_vector))
            pack.sort(key=lambda a: a[1])
            intersection_points = list(map(lambda a: a[0], pack))

            points_b.append(line_b[0])
            points_b.extend(intersection_points)
            points_b.append(line_b[1])

        for line_a in lines_a:
            intersection_points = []
            mu_vector = []
            for line in lines_cutting_off:
                intersection_point, mu = calc_intersection_point_of_two_lines(line, line_a)
                if intersection_point is not None:
                    intersection_points.append(intersection_point)
                    mu_vector.append(mu)
                    intersection_point.visibility = TRANSITIVE

            pack = list(zip(intersection_points, mu_vector))
            pack.sort(key=lambda a: a[1])
            intersection_points = list(map(lambda a: a[0], pack))

            points_a.append(line_a[0])
            points_a.extend(intersection_points)
            points_a.append(line_a[1])

        points_b = points_b[:-1]
        self._determine_points_visibility(fig_b, points_b)
        self._determine_points_visibility(fig_a, points_a)

        self._draw_lines_by_points_with_visibility(points_a, fig_a.color, fig_a.hidden_color)
        self._draw_lines_by_points_with_visibility(points_b, fig_b.color, fig_b.hidden_color)

        for point in points_a:
            point.visibility = None
        for point in points_b:
            point.visibility = None

        # draw_polygon(self._pixels, points_b, fig_b.color)

        # for figure in self._figures:
        #     self._draw_polygon_with_cutting_off(figure)

    def _draw_polygon_with_cutting_off(self, polygon):
        draw_polygon(self._pixels, polygon.points, polygon.color)

    def _draw_lines_by_points_with_visibility(self, points, color, hidden_color):
        lines = make_lines_from_points(points)
        for line in lines:
            if line[0].visibility == VISIBLE or line[1].visibility == VISIBLE:
                draw_line(self._pixels, line[0], line[1], color)
            else:
                draw_line(self._pixels, line[0], line[1], hidden_color)

    def _determine_points_visibility(self, source_figure, points):
        for point in points:
            if point.visibility is not None:
                continue
            for figure in [f for f in self._figures if f.z_order < source_figure.z_order]:
                # if figure == source_figure:
                #     continue
                if figure.is_point_inside(point):
                    point.visibility = HIDDEN
                else:
                    point.visibility = VISIBLE

        for point in points:
            if point.visibility == TRANSITIVE or point.visibility == HIDDEN:
                continue
            if not (self._cutting_off_field.left < point.x < self._cutting_off_field.right):
                point.visibility = HIDDEN
            elif not (self._cutting_off_field.top < point.y < self._cutting_off_field.bottom):
                point.visibility = HIDDEN
            else:
                point.visibility = VISIBLE
