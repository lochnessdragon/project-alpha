import sys, math, os, time
from pathlib import Path

import pygame
from pygame.locals import *
from pygame._sdl2.video import Renderer, Window, Texture

# fix game imports
# directory reach
source_file = Path(__file__)
source_file = source_file.absolute()
print(source_file)

# add parent directory to path
sys.path.append(str(source_file.parent.parent))

# importing
from camera import EditorCamera
import ui

if __name__ == '__main__':
    print("Editor v1")

    assets_dir = str(source_file.parent.parent.joinpath("assets/")) + "/"
    print(assets_dir)

    window = Window("Project Alpha - Editor")
    renderer = Renderer(window, accelerated=1, vsync=True)
    CLEAR_COLOR = Color(100, 100, 100, 255)
    camera = EditorCamera()
    button_0_texture = Texture.from_surface(renderer, pygame.image.load(assets_dir + "img/ui/button_0.png"))
    button_0_patch = ui.NPatchDrawing(button_0_texture, 3, 3, 0, 0, 100, 100)
    test_button = ui.Button(button_0_patch, "Hello, button!")

    # editor main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # tick
        test_button.update()

        # render
        renderer.draw_color = CLEAR_COLOR
        renderer.clear()

        button_0_patch.render()

        renderer.present()
