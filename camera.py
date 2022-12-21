import pygame
from pygame.locals import *
from pygame import Vector2


class Camera:
    """
    Displaces the world around it to simulate a moving camera.
    This is the base class for EditorCamera and PlayerCamera
    """

    def __init__(self, screen_size: (int, int)):
        self.speed = 0.25
        self.position = Vector2(0, 0) # this is the pixel that the center of the camera should be focused on.
        self.scale = 1  # 1:1 mapping of pixel to pixel. lower number is zoomed out, higher number is zoomed in
        self.screen_size = screen_size
        self._half_screen_size = (screen_size[0] // 2, screen_size[1] // 2)

    def update(self, deltaTime: float):
        pass

    def transform(self, rect: Rect) -> Rect:
        return rect.move(self.position.x + self._half_screen_size[0], self.position.y + self._half_screen_size[1])


class EditorCamera(Camera):
    """
    The Camera class that the editor uses
    """

    # def __init__(self, screen_size: (int, int)):
    #     super().__init__(screen_size)

    def update(self, deltaTime: float):
        time_in_ds = deltaTime / 10
        # handle movement events
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            # move left
            self.position.x += self.speed * time_in_ds
        if keys[K_RIGHT] or keys[K_d]:
            # move right
            self.position.x -= self.speed * time_in_ds
        if keys[K_UP] or keys[K_w]:
            # move up
            self.position.y += self.speed * time_in_ds
        if keys[K_DOWN] or keys[K_s]:
            # move down
            self.position.y -= self.speed * time_in_ds

    def on_scroll(self, x: float, y: float):
        """
        on_scroll: react to scroll events by zooming in the camera
        """

        # used so that we can center the zoom on the point the user is at
        mouse_position = pygame.mouse.get_pos()
