import ctypes

import sdl2.ext
import sys
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
            Point(-50, 50),
            Point(50, 50),
            Point(50, -50),
            Point(-50, -50)
        ], sdl2.ext.Color(255, 116, 113, 255), sdl2.ext.Color(255, 200, 50, 255), z_order=2),
        Figure([
            Point(0, 200),
            Point(200, 200),
            Point(100, 0)
        ], sdl2.ext.Color(120, 116, 113, 255), sdl2.ext.Color(35, 116, 174, 255), z_order=1)
    ]
    figures.sort(key=lambda f: f.z_order)

    cutting_off_field = SquareCuttingOffField([
        Point(50, 50),
        Point(590, 50),
        Point(590, 430),
        Point(50, 430)
    ], sdl2.ext.Color(5, 5, 113, 255))

    drawer = Drawer(pixels, cutting_off_field, figures)

    running = True
    old_x = ctypes.c_int32(0)
    old_y = ctypes.c_int32(0)

    last_rotate_time = 0

    is_changed = True

    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                selected_figure_index = None
                SDL_GetMouseState(ctypes.byref(old_x), ctypes.byref(old_y))
                for i in range(len(figures)):
                    print('finding selected figure')
                    if figures[i].is_point_inside(Point(old_x.value, old_y.value)):
                        print('found selected figure')
                        selected_figure_index = i
                        break

            if event.type == sdl2.SDL_MOUSEBUTTONUP:
                selected_figure_index = None

            if event.type == sdl2.SDL_MOUSEMOTION:
                if selected_figure_index is not None:
                    x = ctypes.c_int32(0)
                    y = ctypes.c_int32(0)
                    SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
                    dx = x.value - old_x.value
                    dy = y.value - old_y.value
                    old_x = x
                    old_y = y
                    figures[selected_figure_index].move(dx, dy)
                    is_changed = True

            if event.type == sdl2.SDL_MOUSEWHEEL:
                x = ctypes.c_int32(0)
                y = ctypes.c_int32(0)
                SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
                active_figure = None
                for figure in figures:
                    if figure.is_point_inside(Point(old_x.value, old_y.value)):
                        active_figure = figure
                        break

                if active_figure:
                    active_figure.rotate(event.wheel.y)
                    is_changed = True

        if is_changed:
            clear(window_surface)
            drawer.draw()
            window.refresh()
            is_changed = False

    sdl2.ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())