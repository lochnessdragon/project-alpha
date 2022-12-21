import pygame
from pygame import Vector2
from pygame.locals import *
from pygame._sdl2.video import Renderer, Texture

from .npatchdrawing import NPatchDrawing

class Button:
    def __init__(self, npatch: NPatchDrawing, text: str):
        self.background = npatch
        self.transform = Rect(0, 0, 100, 100)
        self.text = text

    def update(self):
        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            print("Mouse button down!")

    def render(self):
        pass
