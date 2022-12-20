import pygame
from pygame.locals import *
from pygame import Vector2


class Camera:
    """
    Displaces the world around it to simulate a moving camera.
    This is the base class for EditorCamera and PlayerCamera
    """

    def __init__(self):
        self.speed = 0.1
        self.position = Vector2(0, 0)

    def update(self, deltaTime: float):
        pass

    def transform(self, rect: Rect) -> Rect:
        return rect


class EditorCamera(Camera):
    """
    The Camera class that the editor uses
    """

    def __init__(self):
        super().__init__()

    def update(self, deltaTime: float):
        # handle movement events
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            # move left
            self.position.x -= self.speed * deltaTime
        if keys[K_RIGHT] or keys[K_d]:
            # move right
            self.position.x += self.speed * deltaTime
        if keys[K_UP] or keys[K_w]:
            # move up
            self.position.y -= self.speed * deltaTime
        if keys[K_DOWN] or keys[K_s]:
            # move down
            self.position.y += self.speed * deltaTime
