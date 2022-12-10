import sys, math, os, time

import pygame
from pygame.locals import *
from pygame._sdl2.video import Window, Renderer
from entity import Player, TestBall
from spriteset import SpriteSet
from tilemap import Tilemap

# this little line of goodness simply calculates the folder that this file is located in!
# lots of pain has been caused by this line
# do not, under any circumstance:
#       1. modify the line
#       2. expose it to bright lights
#       3. let the line get wet
#       4. or feed the line after midnight
#   without the direction of a senior tech lead.
#   and even so, question the tech leads advice.
# YOU HAVE BEEN WARNED.
root = os.path.dirname(os.path.abspath(__file__))
print(f"Root path: {root}")
# the absolute path to the folder with all the assets
assets_dir = root + "/assets"
# subfolders within the assets directory
tilemap_dir = assets_dir + "/tilemaps/"

# start up the latest and greatest in videogame technology
pygame.init()

# some color defines
BG = Color(53, 249, 252, 255)

# basic window and renderer
window = Window("Project Alpha")
renderer = Renderer(window, accelerated=1, vsync=True)

# game objects
player = Player(renderer, assets_dir)
tilemap = Tilemap.from_file(assets_dir + "/levels/level_00", tilemap_dir, renderer)
#ball = TestBall(renderer, assets_dir)

# used to track elapsed frame time
lastTime = time.time()
while True:
    # calculate the delta time
    currentTime = time.time()
    deltaTime: float = (currentTime - lastTime) * 1000 # time in ms
    lastTime: float = currentTime
    #print(f"{deltaTime} ms") -- could use for stats reporting

    # poll events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # tick
    player.update(deltaTime, tilemap)
    #ball.update(deltaTime)

    # render
    renderer.draw_color = BG
    renderer.clear()

    tilemap.render()
    player.render()
    #ball.render()

    renderer.present()