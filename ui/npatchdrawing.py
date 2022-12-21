import pygame
from pygame import Vector2, Rect
from pygame._sdl2.video import Renderer, Texture


class NPatchDrawing():
    """
    NPatchDrawing - A class to assist in drawing nine-slices.
    Pretty mutch, an image where only a few parts of the image scale and some portions stay the same
    """

    def __init__(self, texture: Texture, insetX, insetY):
        """
        Typical pygame loading function
        initializes the NPatchDrawing class
        """
        self.texture = texture
        self.tex_width = self.texture.width
        self.tex_height = self.texture.height
        self.inset = Vector2(insetX, insetY)

    def render(self, dstrect: Rect):
        """
        render - Draws the NPatchDrawing to the renderer the texture was derived from
        And yes, I did handcode this, and yes, it was pain
        params:
        dstrect: choose where the rectangle is drawn to (allows the texture to be reused by passing around 1 npatch object instead of a new one per each place that needs it)
        """

        # top row
        self.texture.draw(srcrect=Rect(0, 0, self.inset.x, self.inset.y),
                          dstrect=Rect(dstrect.x, dstrect.y,
                                       self.inset.x, self.inset.y))
        self.texture.draw(
            srcrect=Rect(self.inset.x, 0, self.tex_width - (2 * self.inset.x),
                         self.inset.y),
            dstrect=Rect(dstrect.x + self.inset.x, dstrect.y,
                         dstrect.width - (self.inset.x * 2),
                         self.inset.y))
        self.texture.draw(
            srcrect=Rect(self.tex_width - self.inset.x, 0, self.inset.x,
                         self.inset.y),
            dstrect=Rect(
                dstrect.x + dstrect.width - self.inset.x,
                dstrect.y, self.inset.x, self.inset.y))

        # middle row
        self.texture.draw(srcrect=Rect(0, self.inset.y, self.inset.x,
                                       self.tex_height - (self.inset.y * 2)),
                          dstrect=Rect(
                              dstrect.x,
                              dstrect.y + self.inset.y, self.inset.x,
                              dstrect.height - (self.inset.y * 2)))
        self.texture.draw(srcrect=Rect(self.inset.x, self.inset.y,
                                       self.tex_width - (2 * self.inset.x),
                                       self.tex_height - (self.inset.y * 2)),
                          dstrect=Rect(
                              dstrect.x + self.inset.x,
                              dstrect.y + self.inset.y,
                              dstrect.width - (self.inset.x * 2),
                              dstrect.height - (self.inset.y * 2)))
        self.texture.draw(
            srcrect=Rect(self.tex_width - self.inset.x, self.inset.y,
                         self.inset.x, self.tex_height - (self.inset.y * 2)),
            dstrect=Rect(
                dstrect.x + dstrect.width - self.inset.x,
                dstrect.y + self.inset.y, self.inset.x,
                dstrect.height - (self.inset.y * 2)))

        # bottom row
        self.texture.draw(srcrect=Rect(0, self.tex_height - self.inset.y,
                                       self.inset.x, self.inset.y),
                          dstrect=Rect(
                              dstrect.x, dstrect.y +
                              dstrect.height - self.inset.y,
                              self.inset.x, self.inset.y))
        self.texture.draw(
            srcrect=Rect(self.inset.x, self.tex_height - self.inset.y,
                         self.tex_width - (2 * self.inset.x), self.inset.y),
            dstrect=Rect(
                dstrect.x + self.inset.x,
                dstrect.y + dstrect.height - self.inset.y,
                dstrect.width - (self.inset.x * 2), self.inset.y))
        self.texture.draw(
            srcrect=Rect(self.tex_width - self.inset.x,
                         self.tex_height - self.inset.y, self.inset.x,
                         self.inset.y),
            dstrect=Rect(
                dstrect.x + dstrect.width - self.inset.x,
                dstrect.y + dstrect.height - self.inset.y,
                self.inset.x, self.inset.y))
