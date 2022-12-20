import sys, math, os, time

import pygame
from pygame.locals import *
from pygame._sdl2.video import Renderer, Window, Texture

# fix game imports
# directory reach
directory = os.path(__file__).abspath()

# setting path
sys.path.append(directory.parent)

# importing
from camera import EditorCamera

if __name__ == '__main__':
    print("Editor v1")

    window = Window("Project Alpha - Editor")
    renderer = Renderer(window, accelerated=1, vsync=True)
    camera = EditorCamera()

    # editor main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
