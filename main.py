# Spaghetti Code, Spaghetti Code, welcome to my Spaghetti Code!

import sys, math, os, time
from enum import Enum

import pygame
from pygame import Vector2
from pygame.locals import *
from pygame._sdl2.video import Window, Renderer, Texture
from entity import Player, TestBall, PlayerUpdate
from spriteset import SpriteSet
from tilemap import Tilemap
import intro_cutscene as intro
from camera import PlayerCamera
import high_scores
from ui import NPatchDrawing
from input import Input

class GameState(Enum):
    INTRO_SEQ = 1
    PLAY = 2
    HIGH_SCORE_LIST = 3


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
assets_dir = root + "/assets/"
# subfolders within the assets directory
tileset_dir = assets_dir + "tilesets/"

# start up the latest and greatest in videogame technology
pygame.init()

# some color defines
PLAY_BG = Color(237, 173, 78, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)

# basic window and renderer
window = Window("Project Alpha")
window.resizable = True
# load window icon
window_icon = pygame.image.load(assets_dir + "img/ui/window_icon.png")
window.set_icon(window_icon)

# now this probably looks a little different than normal pygame
# that's because we are using sdl2, with HARDWARE ACCELERATED rendering. <explosion effect here>
# GLaDOS believes that we can up fps by a factor of 1000000%, at least in preliminary human tests
renderer = Renderer(window, accelerated=1, vsync=True)

# game objects
tilemap = Tilemap.from_file(assets_dir + "levels/level_00", tileset_dir,
                            renderer)
spawn_pos = Vector2(
    0, 16 * 6
)  # hard coded for now but the hope is to make it derive from data files later
player = Player(renderer, assets_dir, tilemap, spawn_pos)
camera = PlayerCamera(window.size, player, tilemap)

# cool fonts
debug_font = pygame.font.Font(assets_dir + "font/Kenney Pixel.ttf", 16)
small_score_font = pygame.font.Font(assets_dir + "font/Kenney Mini.ttf", 18)
score_font = pygame.font.Font(assets_dir + "font/Kenney Mini.ttf", 32)
score_header_font = pygame.font.Font(assets_dir + "font/Kenney Mini.ttf", 48)

# intro animation object
intro_scene = intro.IntroCutscene(assets_dir, renderer, debug_font,
                                  assets_dir + "font/Kenney Future.ttf",
                                  window.size)

# background sprite assets
earth_image = Texture.from_surface(
    renderer,
    pygame.transform.scale(pygame.image.load(assets_dir + "img/bg/earth.png"),
                           (32, 32)))
earth_image.alpha = 200
earth_image_rect = earth_image.get_rect()
earth_image_rect.centerx = (window.size[0] // 6) * 5
earth_image_rect.centery = (window.size[1] // 6)

background_image = Texture.from_surface(
    renderer,
    pygame.image.load(assets_dir + "img/bg/parallax/desert-bg-0.png"))
background_image_rect = background_image.get_rect()
background_image_rect.centerx = window.size[0] // 2
background_image_rect.centery = window.size[1] // 2

# store state
state = GameState.PLAY

# score information
score = 0
name = ""
(top_names, top_scores) = high_scores.get_high_scores()
needs_name_input = True
name_prompt_bg = NPatchDrawing(
    Texture.from_surface(
        renderer,
        pygame.image.load(assets_dir + "img/ui/prompt_background.png")), 2, 2)
# keeps track of an error that says that the name is too short
show_name_enter_error_timer = 0

# used to track elapsed frame time
lastTime = time.time()

# used to keep track of the level time (in ms)
level_time = 3 * 60 * 1000  # 3 minutes
# keeps track of the coins collected
level_score = 0

Input.init()

while True:
    # calculate the delta time
    currentTime = time.time()
    deltaTime: float = (currentTime - lastTime) * 1000  # time in ms
    lastTime: float = currentTime
    #print(f"{deltaTime} ms") -- could use for stats reporting

    # poll events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == VIDEORESIZE:
            print(f"Resized Window: X: {event.w} Y: {event.h}")
            camera.on_resize(event.w, event.h)
        if event.type == KEYDOWN:
            if state == GameState.HIGH_SCORE_LIST:
                if needs_name_input:
                    # change name
                    # if its a valid character
                    if event.unicode.isprintable():
                        if len(name) < 5:
                            name += event.unicode.upper()
                    else:
                        # its a key press
                        if event.key == K_BACKSPACE:
                            # delete a character
                            name = name[:-1]
                        elif event.key == K_RETURN:
                            # submit the name if its filled out the whole string
                            if len(name) == 5:
                                print(f"User entered name: {name}")
                                needs_name_input = False # no more name needed
                                (top_names,
                                 top_scores) = high_scores.add_high_score(
                                     name, score) # update the high scores list
                            else:
                                # show an error if they need to enter more letters
                                show_name_enter_error_timer = 2000  # two seconds
                else:
                    # key press
                    if event.key == K_r:
                        # reset level (this should be abstracted into a function but crunch gets us all :P)
                        state = GameState.PLAY
                        player.transform.x = spawn_pos.x
                        player.transform.y = spawn_pos.y
                        name = ""
                        needs_name_input = False
                        score = 0
                        level_score = 0
                        level_time = 3 * 60 * 1000  # 3 minutes
                        tilemap.reset()
    # tick
    Input.update() # update the input system

    if state == GameState.PLAY:
        level_time -= deltaTime # keeps track of the elapsed time in the level
        (added_score, player_state) = player.update(deltaTime, tilemap) # move the player
        level_score += added_score # add some score

        # stop when out of tile
        if level_time < 0:
            player_state = PlayerUpdate.DIED # rut roo, out of time

        if player_state == PlayerUpdate.DIED:
            # reset player (same as above)
            player.transform.x = spawn_pos.x
            player.transform.y = spawn_pos.y
            name = ""
            needs_name_input = False
            score = 0
            level_score = 0
            level_time = 3 * 60 * 1000  # 3 minutes
            tilemap.reset()

        # if won
        if player_state == PlayerUpdate.WON:
            state = GameState.HIGH_SCORE_LIST # show dem scores
            # player score calc
            score = level_score + int(
                level_time //
                50)  # coins picked up and the leftover time in seconds
            print(f"Player achieved score: {score}")
            # see if its a new high score
            if high_scores.get_score_index(score,
                                           top_scores) < 5:  # new high score!
                needs_name_input = True
                name = ""

        # move the follow camera towards the player
        camera.update(deltaTime)
    elif state == GameState.INTRO_SEQ:
        # more animation
        if intro_scene.update(deltaTime):
            # animation is done
            state = GameState.PLAY
    elif state == GameState.HIGH_SCORE_LIST:
        # tick down the error message
        if needs_name_input and show_name_enter_error_timer > 0:
            show_name_enter_error_timer -= deltaTime

    # render
    # clear color
    if state == GameState.PLAY:
        renderer.draw_color = PLAY_BG
    elif state == GameState.INTRO_SEQ:
        renderer.draw_color = intro.CLEAR_COLOR
    elif state == GameState.HIGH_SCORE_LIST:
        # black background
        renderer.draw_color = Color(0, 0, 0, 255)

    renderer.clear()

    if state == GameState.PLAY:
        # render background
        background_image.draw(dstrect=background_image_rect)
        earth_image.draw(dstrect=earth_image_rect, angle=-25)

        # render tilemap
        tilemap.render(camera)

        # render player
        player.render(camera)

        # render ui
        # render score
        score_texture = Texture.from_surface(
            renderer,
            small_score_font.render(f"Score: {level_score}", True, WHITE))
        score_texture.draw(dstrect=score_texture.get_rect())

        # render the time left
        minutes = int(level_time / (60 * 1000))
        seconds = int((level_time / 1000) % 60)
        time_texture = Texture.from_surface(
            renderer,
            small_score_font.render(f"Time: {minutes}:{seconds:02}", True, WHITE))
        time_texture_rect = time_texture.get_rect()
        time_texture_rect.x = window.size[0] - time_texture_rect.width # right side of the screen
        time_texture.draw(dstrect=time_texture_rect)

        # debug info
        debug_text = Texture.from_surface(
            renderer,
            small_score_font.render("MS/F: {:.2f}".format(deltaTime), False,
                                    WHITE))
        debug_text.draw(dstrect=debug_text.get_rect().move(0, 20))

        player_stats = Texture.from_surface(renderer, small_score_font.render(f"Position: x={player.transform.x:.2f} y={player.transform.y:.2f} Velocity: x={player.collider.velocity.x:.2f} y={player.collider.velocity.y:.2f}", False, WHITE))
        player_stats.draw(dstrect=player_stats.get_rect().move(0, 40))
    elif state == GameState.INTRO_SEQ:
        intro_scene.render() # abstraction, hooray!
    elif state == GameState.HIGH_SCORE_LIST:
        # show the list of scores
        header = Texture.from_surface(
            renderer, score_header_font.render("High Scores:", True, WHITE))
        header_rect = header.get_rect()
        header_rect.centerx = window.size[0] // 2 # center header
        header_rect.y = window.size[1] // 6 # at the top of the screen
        header.draw(dstrect=header_rect)

        for score_index in range(len(top_names)):
            score_str = f"{score_index + 1}. {top_names[score_index]}......{top_scores[score_index]}" # retro formatting
            score_texture = Texture.from_surface(
                renderer, score_font.render(score_str, True, WHITE))
            score_rect = score_texture.get_rect()
            score_rect.centerx = window.size[0] // 2 # center the score

            # show the scores in a list
            score_rect.y = (
                score_index *
                (score_rect.height + 5)) + header_rect.height + header_rect.y

            score_texture.draw(dstrect=score_rect)

        if needs_name_input:
            # draw input box with the name

            # draw the background
            bounding_rect = Rect(0, 0, 256, 156)
            bounding_rect.centerx = window.size[0] // 2
            bounding_rect.centery = window.size[1] // 2
            name_prompt_bg.render(bounding_rect)

            # draw the prompt header
            prompt_texture = Texture.from_surface(
                renderer,
                small_score_font.render("Enter your name:", True, WHITE))
            prompt_texture_rect = prompt_texture.get_rect()
            prompt_texture_rect.centerx = window.size[0] // 2 # centered
            prompt_texture_rect.centery = (window.size[1] // 2) - (
                1.5 * prompt_texture_rect.height) # top of the box
            prompt_texture.draw(dstrect=prompt_texture_rect)

            # draw the currently entered name (formatted, of course)
            name_formatted = ""
            for i in range(5):
                if i < len(name):
                    name_formatted += name[i]
                else:
                    name_formatted += "_"
                if i != 4:
                    name_formatted += " "

            name_texture = Texture.from_surface(
                renderer, score_font.render(name_formatted, True, WHITE))
            name_rect = name_texture.get_rect()

            name_rect.centerx = window.size[0] // 2 # centered
            name_rect.centery = window.size[1] // 2 # centered
            name_texture.draw(dstrect=name_rect)

            # if there is an error, we also want to show that
            if show_name_enter_error_timer > 0:
                error_texture = Texture.from_surface(
                    renderer,
                    score_font.render(" Your name must be 5 characters long. ",
                                      True, WHITE, RED))
                error_texture_rect = error_texture.get_rect()
                error_texture_rect.centerx = window.size[0] // 2
                error_texture_rect.y = window.size[
                    1] - error_texture_rect.height
                error_texture.draw(dstrect=error_texture_rect)
        else:
            # if the user has entered their name, then they can restart
            restart_prompt = Texture.from_surface(
                renderer, score_font.render("Press R to restart.", True,
                                            WHITE))
            restart_prompt_rect = restart_prompt.get_rect()
            restart_prompt_rect.centerx = window.size[0] // 2
            restart_prompt_rect.centery = (window.size[1] // 6) * 5
            restart_prompt.draw(dstrect=restart_prompt_rect)

    # somehow, this little function takes on average ~26 ms to run on repl.it
    renderer.present()
