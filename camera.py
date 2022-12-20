import pygame
from pygame.locals import *

class Camera:
    """
    Displaces the world around it to simulate a moving camera.
    This is the base class for EditorCamera and PlayerCamera
    """
    def __init__(self):
        self.speed = 0.1

    def update(self):
        self.position = (0, 0)

    def transform(self, rect: Rect) -> Rect:
        return rect

class EditorCamera(Camera):
    """
    The Camera class that the editor uses
    """
    def __init__(self):
        super().__init__()

    def update(self):
        # handle movement events
