from graphics import calc_intersection_point_of_two_lines, Point

assert (Point(75, 75) == calc_intersection_point_of_two_lines(
    [Point(100, 100), Point(50, 50)],
    [Point(50, 100), Point(100, 50)]
)[0]), 'Incorrect intersection point'
