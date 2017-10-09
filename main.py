import ctypes

import sdl2.ext
import sys

import time
from sdl2 import *
from sdl2.examples.pixelaccess import BLACK

from drawer import Drawer
from figure import Figure, SquareCuttingOffField
from graphics import draw_line, Point, draw_polygon

selected_figure_index = None


def clear(surface):
    sdl2.ext.fill(surface, BLACK)


def main():
    global selected_figure_index

    sdl2.ext.init()
    window = sdl2.ext.Window("Filled polygon", size=(640, 480))
    window.show()

    window_surface = window.get_surface()
    pixels = sdl2.ext.PixelView(window_surface)

    figures = [
        Figure([
            Point(250, 200),
            Point(380, 200),
            Point(380, 310),
            Point(250, 310)
        ], sdl2.ext.Color(0, 255, 0, 255), sdl2.ext.Color(255, 255, 255, 255), z_order=1),
        Figure([
            Point(330, 250),
            Point(400, 300),
            Point(160, 300)
        ], sdl2.ext.Color(0, 0, 255, 255), sdl2.ext.Color(255, 255, 255, 255), z_order=2)
    ]
    figures.sort(key=lambda f: f.z_order)

    cutting_off_field = SquareCuttingOffField(50, 590, 430, 50, sdl2.ext.Color(255, 0, 0, 255))

    drawer = Drawer(pixels, cutting_off_field, figures)

    running = True
    old_x = ctypes.c_int32(0)
    old_y = ctypes.c_int32(0)

    last_rotate_time = 0

    is_changed = True

    frame_interval = 0.001

    last_time = time.time()
    dy = [1, -1]
    animation_y_boards = [[200, 300], [200, 300]]

    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            # if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            #     selected_figure_index = None
            #     SDL_GetMouseState(ctypes.byref(old_x), ctypes.byref(old_y))
            #     for i in range(len(figures)):
            #         if figures[i].is_point_inside(Point(old_x.value, old_y.value)):
            #             selected_figure_index = i
            #             break
            #
            # if event.type == sdl2.SDL_MOUSEBUTTONUP:
            #     selected_figure_index = None
            #
            # if event.type == sdl2.SDL_MOUSEMOTION:
            #     if selected_figure_index is not None:
            #         x = ctypes.c_int32(0)
            #         y = ctypes.c_int32(0)
            #         SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
            #         dx = x.value - old_x.value
            #         dy = y.value - old_y.value
            #         old_x = x
            #         old_y = y
            #         figures[selected_figure_index].move(dx, dy)
            #         is_changed = True
            #
            # if event.type == sdl2.SDL_MOUSEWHEEL:
            #     x = ctypes.c_int32(0)
            #     y = ctypes.c_int32(0)
            #     SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
            #     active_figure = None
            #     for figure in figures:
            #         if figure.is_point_inside(Point(old_x.value, old_y.value)):
            #             active_figure = figure
            #             break
            #
            #     if active_figure:
            #         active_figure.rotate(event.wheel.y)
            #         is_changed = True

        now = time.time()

        if now - last_time >= frame_interval:
            for i in range(len(figures)):
                figures[i].move(0, dy[i])
                is_changed = True
                if figures[i].points[0].y > animation_y_boards[i][1] or figures[i].points[0].y < animation_y_boards[i][0]:
                    dy[i] *= -1
            last_time = now


        if is_changed:
            clear(window_surface)
            drawer.draw()
            window.refresh()
            is_changed = False

    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())