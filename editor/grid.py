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
        self.renderer.draw_color = self.grid_color

        # draw vertical lines
        # custom for loop to avoid numpy dependence

        # technically 0 for a steady camera, but we need an offset from the left of the screen
        # campos % grid_spacing is the difference between the camera and the correct grid line pos
        x: float = -camera.position.x * camera.scale #(int(-camera.position.x) % (self.grid_spacing * camera.scale)) * -camera.scale

        max_x = self._screen_size[0]
        step_x = self.grid_spacing * camera.scale
        while x <= max_x:
            self.renderer.draw_line((x, 0), (x, self._screen_size[1]))
            x += step_x

        # draw horizontal lines
        y = int(camera.position.y) % (self.grid_spacing * camera.scale)
        max_y = self._screen_size[1]
        step_y = self.grid_spacing * camera.scale
        while y <= max_y:
            self.renderer.draw_line((0, y), (self._screen_size[0], y))
            y += step_y
