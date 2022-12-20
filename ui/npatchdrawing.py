import pygame
from pygame import Vector2, Rect
from pygame._sdl2.video import Renderer, Texture


class NPatchDrawing():
    """
    NPatchDrawing - A class to assist in drawing nine-slices.
    Pretty mutch, an image where only a few parts of the image scale and some portions stay the same
    """

    def __init__(self, texture: Texture, insetX, insetY, posX, posY, width,
                 height):
        """
        Typical pygame loading function
        initializes the NPatchDrawing class
        """
        self.texture = texture
        self.tex_width = self.texture.width
        self.tex_height = self.texture.height
        self.inset = Vector2(insetX, insetY)
        self.transform = Rect(posX, posY, width, height)

    def render(self):
        """
        render - Draws the NPatchDrawing to the renderer the texture was derived from
        And yes, I did handcode this, and yes, it was pain
        """

        # top row
        self.texture.draw(srcrect=Rect(0, 0, self.inset.x, self.inset.y),
                          dstrect=Rect(self.transform.x, self.transform.y,
                                       self.inset.x, self.inset.y))
        self.texture.draw(
            srcrect=Rect(self.inset.x, 0, self.tex_width - (2 * self.inset.x),
                         self.inset.y),
            dstrect=Rect(self.transform.x + self.inset.x, self.transform.y,
                         self.transform.width - (self.inset.x * 2),
                         self.inset.y))
        self.texture.draw(
            srcrect=Rect(self.tex_width - self.inset.x, 0, self.inset.x,
                         self.inset.y),
            dstrect=Rect(
                self.transform.x + self.transform.width - self.inset.x,
                self.transform.y, self.inset.x, self.inset.y))

        # middle row
        self.texture.draw(srcrect=Rect(0, self.inset.y, self.inset.x,
                                       self.tex_height - (self.inset.y * 2)),
                          dstrect=Rect(
                              self.transform.x,
                              self.transform.y + self.inset.y, self.inset.x,
                              self.transform.height - (self.inset.y * 2)))
        self.texture.draw(srcrect=Rect(self.inset.x, self.inset.y,
                                       self.tex_width - (2 * self.inset.x),
                                       self.tex_height - (self.inset.y * 2)),
                          dstrect=Rect(
                              self.transform.x + self.inset.x,
                              self.transform.y + self.inset.y,
                              self.transform.width - (self.inset.x * 2),
                              self.transform.height - (self.inset.y * 2)))
        self.texture.draw(
            srcrect=Rect(self.tex_width - self.inset.x, self.inset.y,
                         self.inset.x, self.tex_height - (self.inset.y * 2)),
            dstrect=Rect(
                self.transform.x + self.transform.width - self.inset.x,
                self.transform.y + self.inset.y, self.inset.x,
                self.transform.height - (self.inset.y * 2)))

        # bottom row
        self.texture.draw(srcrect=Rect(0, self.tex_height - self.inset.y,
                                       self.inset.x, self.inset.y),
                          dstrect=Rect(
                              self.transform.x, self.transform.y +
                              self.transform.height - self.inset.y,
                              self.inset.x, self.inset.y))
        self.texture.draw(
            srcrect=Rect(self.inset.x, self.tex_height - self.inset.y,
                         self.tex_width - (2 * self.inset.x), self.inset.y),
            dstrect=Rect(
                self.transform.x + self.inset.x,
                self.transform.y + self.transform.height - self.inset.y,
                self.transform.width - (self.inset.x * 2), self.inset.y))
        self.texture.draw(
            srcrect=Rect(self.tex_width - self.inset.x,
                         self.tex_height - self.inset.y, self.inset.x,
                         self.inset.y),
            dstrect=Rect(
                self.transform.x + self.transform.width - self.inset.x,
                self.transform.y + self.transform.height - self.inset.y,
                self.inset.x, self.inset.y))
