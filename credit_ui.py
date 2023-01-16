# I wanted to implement this but I didn't have time to
import pygame
from pygame.locals import *
from pygame._sdl2.video import Renderer, Texture, Window

class CreditsUI:
    """
    Displays the credits for the game
    Using semi-markdown rules to translate # to h1, ## to h2, ### to h3
    Underlies h1s with ===========
    Also needs to respect spacing between the lines and proper formatting
    """
    def __init__(self, assets_dir: str, renderer: Renderer, h1_font: Font, h2_font: Font, h3_font: Font, default_font: Font):
        self.lines = []
        with open(assets_dir + "credits.txt") as file:
            for line in file.readlines():
                self.lines.append(line.strip())

        self.timer = 0
        self.renderer = renderer 
        self.h1_font = h1_font
        self.h2_font = h2_font 
        self.h3_font = h3_font 
        self.default_font = default_font
        # stores a list of all the text elements in use (texture + rect)
        self.surfaces = []

    def tick(deltaTime: float):
        self.timer += deltaTime 

        for index in range(len(self.surfaces)):
            pass
    
    def render():
        pass


if __name__ == "__main__":
    creditsui = CreditsUI("assets/")