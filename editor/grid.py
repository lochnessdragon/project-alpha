import pygame
from pygame.locals import *
from pygame._sdl2.video import Renderer, Texture
from pygame import Vector2

from camera import Camera


class Grid:
    """
    Grid - utility class to draw a grid for the editor
    """

    def __init__(self, renderer: Renderer, grid_color: Color,
                 grid_spacing: int, window_size: (int, int)):
        """
        grid_spacing: the number of pixels between each grid line
        """
        self.renderer = renderer
        self.grid_spacing = grid_spacing
        self.grid_color = grid_color
        self._screen_size = window_size

    def render(self, camera: Camera):
        # this will be a painful method

        self.renderer.draw_color = self.grid_color
        # draw vertical lines
        for x in range(int(camera.position.x) % self.grid_spacing,
                       self._screen_size[0], self.grid_spacing):
            self.renderer.draw_line((x, 0), (x, self._screen_size[1]))

        # draw horizontal lines
        for y in range(int(camera.position.y) % self.grid_spacing,
                       self._screen_size[1], self.grid_spacing):
            self.renderer.draw_line((0, y), (self._screen_size[0], y))
        pass
