from figure import make_lines_from_points
from graphics import draw_line, draw_polygon, calc_intersection_point_of_two_lines

VISIBLE = 'visible'
HIDDEN = 'hidden'
TRANSITIVE = 'transitive'
TO_VISIBLE = 'to visible'
TO_HIDDEN = 'to hidden'

CUTTING_OUT_FIELD = 1
FIGURE = 2

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
            for line in lines_a:
                intersection_point, mu = calc_intersection_point_of_two_lines(line, line_b)
                if intersection_point is not None:
                    intersection_points.append(intersection_point)
                    mu_vector.append(mu)
                    intersection_point.visibility = TRANSITIVE
                    # intersection_point.hidden_by |= FIGURE
                    intersection_point.with_ = FIGURE

            for line in lines_cutting_off:
                intersection_point, mu = calc_intersection_point_of_two_lines(line, line_b)
                if intersection_point is not None:
                    intersection_points.append(intersection_point)
                    mu_vector.append(mu)
                    intersection_point.visibility = TRANSITIVE
                    # intersection_point.hidden_by |= CUTTING_OUT_FIELD
                    intersection_point.with_ = CUTTING_OUT_FIELD

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
                    # intersection_point.hidden_by |= CUTTING_OUT_FIELD
                    intersection_point.with_ = CUTTING_OUT_FIELD

            pack = list(zip(intersection_points, mu_vector))
            pack.sort(key=lambda a: a[1])
            intersection_points = list(map(lambda a: a[0], pack))

            points_a.append(line_a[0])
            points_a.extend(intersection_points)
            points_a.append(line_a[1])

        points_a = self._unique_points(points_a)
        points_b = self._unique_points(points_b)

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

    def _unique_points(self, points):
        res = []
        for point in points:
            if point in res:
                continue
            res.append(point)
        return res

    def _draw_polygon_with_cutting_off(self, polygon):
        draw_polygon(self._pixels, polygon.points, polygon.color)

    def _draw_lines_by_points_with_visibility(self, points, color, hidden_color):
        lines = make_lines_from_points(points)
        for line in lines:
            if line[0].visibility == VISIBLE\
                    or line[0].visibility == TO_VISIBLE:
                draw_line(self._pixels, line[0], line[1], color)
            else:
                draw_line(self._pixels, line[0], line[1], hidden_color)

    def _determine_points_visibility(self, source_figure, points):
        for point in points:
            for figure in [f for f in self._figures if f.z_order < source_figure.z_order]:
                if figure.is_point_inside(point):
                    point.hidden_by |= FIGURE
                    if point.visibility is not None:
                        continue
                    point.visibility = HIDDEN
                else:
                    if point.visibility is not None:
                        continue
                    point.visibility = VISIBLE

        for point in points:
            if self._cutting_off_field.is_point_hidden(point):
                point.visibility = HIDDEN
                point.hidden_by |= CUTTING_OUT_FIELD
            else:
                point.visibility = VISIBLE if point.visibility is None else point.visibility

        for i in range(len(points)):
            point = points[i]
            next_point = points[(i + 1) % len(points)]
            prev_point = points[(i - 1)]

            if point.visibility == TRANSITIVE and next_point.visibility == TRANSITIVE:
                point_cs_code = self._cutting_off_field.get_cohen_sutherland_code_for_point(point)
                next_point_cs_code = self._cutting_off_field.get_cohen_sutherland_code_for_point(next_point)

                if (point_cs_code != 0 and next_point_cs_code != 0) and point_cs_code & next_point_cs_code == 0 and point.hidden_by & FIGURE == 0:
                    point.visibility = VISIBLE
                    continue
                elif (point_cs_code == 0 and next_point_cs_code != 0) and point_cs_code & next_point_cs_code == 0:
                    # not (
                    # source_figure.is_point_inside(point) and self._cutting_off_field.is_point_hidden(next_point)) and
                    if point.with_ == FIGURE and next_point.with_ == CUTTING_OUT_FIELD and \
                             (prev_point.visibility != VISIBLE and prev_point.visibility != TO_VISIBLE):
                        point.visibility = TO_VISIBLE
                    continue
                elif (point_cs_code != 0 and next_point_cs_code == 0) and point_cs_code & next_point_cs_code == 0:
                    if point.with_ == CUTTING_OUT_FIELD and next_point.with_ == FIGURE and point.hidden_by & FIGURE == 0:
                        point.visibility = TO_VISIBLE
                    continue

                elif point_cs_code != 0 and point_cs_code == next_point_cs_code:
                    point.visibility = HIDDEN
                    continue

            if point.visibility == TRANSITIVE and next_point.visibility == VISIBLE:
                point.visibility = TO_VISIBLE
                continue

            if point.visibility == TRANSITIVE and next_point.visibility == HIDDEN:
                point.visibility = TO_HIDDEN
                continue

