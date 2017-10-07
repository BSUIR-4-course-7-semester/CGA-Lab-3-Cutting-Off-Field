from sdl2 import SDL_Point


class Point(SDL_Point):
    def __add__(self, value):
        return Point(self.x + value.x, self.y + value.y)