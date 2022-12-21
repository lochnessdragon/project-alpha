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
from tilemap import Tilemap
import ui
import grid

if __name__ == '__main__':
    print("Editor v1")
    pygame.init()

    assets_dir = str(source_file.parent.parent.joinpath("assets/")) + "/"
    print(assets_dir)

    window = Window("Project Alpha - Editor")
    renderer = Renderer(window, accelerated=1, vsync=True)
    CLEAR_COLOR = Color(50, 50, 50, 255)
    camera = EditorCamera(window.size)
    button_0_texture = Texture.from_surface(
        renderer, pygame.image.load(assets_dir + "img/ui/button_0.png"))
    button_0_patch = ui.NPatchDrawing(button_0_texture, 3, 3)
    button_font = pygame.font.Font(assets_dir + "font/Kenney Blocks.ttf", 12)
    test_button = ui.Button(renderer, button_0_patch, button_font,
                            "Hello, button!", 4,
                            (255, 255, 255))  # 4px padding
    test_button.posx = 20
    test_button.posy = 20

    # editor grid
    grid = grid.Grid(renderer, Color(255, 255, 255, 255), 16, window.size)

    # load default tilemap
    tilemap_filename = assets_dir + "/levels/level_00"
    tilemap = Tilemap.from_file(tilemap_filename, assets_dir + "tilesets/",
                                renderer)

    # editor main loop
    lastTime = time.time()
    while True:
        # calculate the delta time
        currentTime = time.time()
        deltaTime: float = (currentTime - lastTime) * 1000  # time in ms
        lastTime: float = currentTime

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEWHEEL:
                camera.on_scroll(event.x, event.y)
            elif event.type == KEYDOWN:
                if event.key == K_s && (event.mod & KMOD_CTRL):
                    print("Saving tilemap")
                    tilemap.save(tilemap_filename)

        # tick
        camera.update(deltaTime)

        # render
        renderer.draw_color = CLEAR_COLOR
        renderer.clear()

        # render tilemap and grid overlay
        tilemap.render(camera)
        grid.render(camera)

        renderer.present()
