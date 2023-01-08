import pygame
from pygame import Vector2
from pygame.locals import *
from pygame._sdl2.video import Renderer, Texture

from .npatchdrawing import NPatchDrawing


class Button:
    """
    Button - A UI Component that is 
             interactable with the mouse.
    """

    def __init__(self, renderer: Renderer, npatch: NPatchDrawing, 
                 pressed_npatch: NPatchDrawing, font: pygame.font.Font, 
                 text: str, padding: int, text_color: (int, int, int)):
        self.background = npatch
        self.background_pressed = pressed_npatch
        self.is_selected = False

        self._texture = Texture.from_surface(
            renderer, font.render(text, True, text_color))
        self._texture_rect = self._texture.get_rect()

        self.transform = Rect(0, 0, self._texture.width + (2 * padding),
                              self._texture.height + (2 * padding))
        self._texture_rect.centerx = self.transform.centerx
        self._texture_rect.centery = self.transform.centery

        self.renderer = renderer
        self._text = text
        self.padding = padding
        self.text_color = text_color
        self.text_font = font

    # getters and setters for the text to update the surface/transform
    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str):
        print("Setting the text")
        self._text = text
        self._texture = Texture.from_surface(
            self.renderer, self.text_font.render(text, True, self.text_color))
        self._texture_rect = self._texture.get_rect()

        self.transform = Rect(0, 0, self._texture.width + (2 * self.padding),
                              self._texture.height + (2 * self.padding))
        self._texture_rect.centerx = self.transform.centerx
        self._texture_rect.centery = self.transform.centery

    # getters and setters for the button position
    @property
    def posx(self) -> float:
        return self.transform.x

    @posx.setter
    def posx(self, x: float):
        self.transform.x = x
        self._texture_rect.centerx = self.transform.centerx

    @property
    def posy(self) -> float:
        return self.transform.y

    @posy.setter
    def posy(self, y: float):
        self.transform.y = y
        self._texture_rect.centery = self.transform.centery
    
    # texture getters/setters
    @property 
    def texture(self) -> Texture:
        return self._texture
    
    @texture.setter 
    def texture(self, texture: Texture):
        self._texture = texture 
        self._texture_rect = self._texture.get_rect()
        self.transform.width = self._texture.width + (2 * self.padding)
        self.transform.height = self._texture.height + (2 * self.padding)


    def update(self):
        if self.transform.collidepoint(pygame.mouse.get_pos()):
            self.is_selected = True
        else:
            self.is_selected = False
        self._texture_rect.centerx = self.transform.centerx
        self._texture_rect.centery = self.transform.centery
        
    def render(self):
        # draw background
        if not self.is_selected:
            self.background.render(self.transform)
        else:
            self.background_pressed.render(self.transform)

        # draw text
        self._texture.draw(dstrect=self._texture_rect)
