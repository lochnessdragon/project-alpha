import sys, math, os, time
from enum import Enum

import pygame
from pygame.locals import *
from pygame._sdl2.video import Window, Renderer
from entity import Player, TestBall
from spriteset import SpriteSet
from tilemap import Tilemap
import intro_cutscene as intro

class GameState(Enum):
    INTRO_SEQ = 1
    PLAY = 2

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
PLAY_BG = Color(237, 173, 78, 255)

# basic window and renderer
window = Window("Project Alpha")
renderer = Renderer(window, accelerated=1, vsync=True)

# game objects
player = Player(renderer, assets_dir)
tilemap = Tilemap.from_file(assets_dir + "/levels/level_00", tilemap_dir, renderer)
#ball = TestBall(renderer, assets_dir)

# cool fonts
debug_font = pygame.font.Font(assets_dir + "/font/Kenney Pixel.ttf", 16)

# intro animation object
intro_scene = intro.IntroCutscene(assets_dir, renderer, debug_font, assets_dir + "/font/Kenney Future.ttf", window.size)

state = GameState.PLAY

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
    if state == GameState.PLAY:
        player.update(deltaTime, tilemap)
    elif state == GameState.INTRO_SEQ:
        if intro_scene.update(deltaTime):
            # animation is done
            state = GameState.PLAY
    #ball.update(deltaTime)

    # render
    if state == GameState.PLAY:
        renderer.draw_color = PLAY_BG
    elif state == GameState.INTRO_SEQ:
        renderer.draw_color = intro.CLEAR_COLOR

    renderer.clear()

    if state == GameState.PLAY:
        tilemap.render()
        player.render()
    elif state == GameState.INTRO_SEQ:
        intro_scene.render()
    #ball.render()

    renderer.present()
