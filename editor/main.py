import sys 

import pygame
from pygame.locals import *
from pygame._sdl2.video import Window, Renderer, Texture

# used to allow the editor to become a standalone interface
if __name__ == '__main__':
    print("Editor v1")
    BG = (100, 100, 100, 255)
    pygame.init();
    window = Window("Project Alpha - Editor")
    renderer = Renderer(window, acclerated = 1, vsync = True)

    button1 = Button("Create tilemap")

    while True:
        # event poll
        for event in pygame.event.get():
            if event == QUIT:
                pygame.quit()
                sys.exit()
        # tick

        # update
        renderer.draw_color = BG
        renderer.clear()



        renderer.present()

