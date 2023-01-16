# this is some cool editor code. Try it if you like! :)

import sys, math, os, time
from enum import Enum
from pathlib import Path

import pygame
from pygame.locals import *
from pygame._sdl2.video import Renderer, Window, Texture
from pygame import Vector2

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

class BrushType(Enum):
    """
    Represents different valid brush types
    """
    PENCIL = 1
    EYEDROPPER = 2
    ERASER = 3
    FILL = 4

def flood_fill(pos_x: int, pos_y: int, tilemap: Tilemap, original_tile_id: int, new_tile_id: int):
    """
    An implementation of the flood fill algorithm. Used for the bucket fill tool
    """
    if pos_x < tilemap._width and pos_x >= 0 and pos_y < tilemap._height and pos_y >= 0 and tilemap.get_tile(pos_x, pos_y) == original_tile_id:
        tilemap.set_tile(pos_x, pos_y, new_tile_id)
        flood_fill(pos_x + 1, pos_y, tilemap, original_tile_id, new_tile_id)
        flood_fill(pos_x - 1, pos_y, tilemap, original_tile_id, new_tile_id)
        flood_fill(pos_x, pos_y + 1, tilemap, original_tile_id, new_tile_id)
        flood_fill(pos_x, pos_y - 1, tilemap, original_tile_id, new_tile_id)


if __name__ == '__main__':
    print("Editor v1")
    pygame.init()

    # find the assets directory
    assets_dir = str(source_file.parent.parent.joinpath("assets/")) + "/"
    print(assets_dir)

    # basic screen stuff
    window = Window("Project Alpha - Editor")
    half_screen_size = (window.size[0] // 2, window.size[1] // 2)

    # load window icon
    window_icon = pygame.image.load(assets_dir + "img/ui/window_icon.png")
    window.set_icon(window_icon)

    # basic rendering things (_sdl2 in pygame. OOOOHHH experimental)
    renderer = Renderer(window, accelerated=1, vsync=True)
    CLEAR_COLOR = Color(50, 50, 50, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    camera = EditorCamera(window.size)

    # brush type
    brush_type = BrushType.PENCIL

    # fonts
    button_font = pygame.font.Font(assets_dir + "font/Kenney Blocks.ttf", 12)
    info_font = pygame.font.SysFont("Cascadia Mono", 16)

    # icons
    draw_icon = Texture.from_surface(renderer, pygame.image.load(
        assets_dir + "img/ui/draw_tile_icon.png"))
    eyedropper_icon = Texture.from_surface(
        renderer, pygame.image.load(assets_dir + "img/ui/eyedropper_icon.png"))
    eraser_icon = Texture.from_surface(
        renderer, pygame.image.load(assets_dir + "img/ui/eraser_icon.png"))
    bucket_fill_icon = Texture.from_surface(renderer, pygame.image.load(assets_dir + "img/ui/fill_icon.png"))

    # buttons
    button_0_texture = Texture.from_surface(
        renderer, pygame.image.load(assets_dir + "img/ui/button_0.png"))
    button_0_patch = ui.NPatchDrawing(button_0_texture, 3, 3)
    button_0_pressed_texture = Texture.from_surface(
        renderer, pygame.image.load(assets_dir + "img/ui/button_0_pressed.png"))
    button_0_pressed_patch = ui.NPatchDrawing(button_0_pressed_texture, 3, 3)

    def pencil_button_press():
        global brush_type
        brush_type = BrushType.PENCIL
    pencil_button = ui.Button(renderer, button_0_patch, button_0_pressed_patch, button_font,
                              "Pencil", 4,
                              WHITE, pencil_button_press)  # 4px padding
    pencil_button.texture = draw_icon

    def eyedropper_button_press():
        global brush_type
        brush_type = BrushType.EYEDROPPER
    eyedropper_button = ui.Button(renderer, button_0_patch, button_0_pressed_patch,
                                  button_font, "Eyedropper", 4, WHITE, eyedropper_button_press)
    eyedropper_button.texture = eyedropper_icon
    eyedropper_button.posy += pencil_button.transform.height

    def eraser_button_press():
        global brush_type
        brush_type = BrushType.ERASER
    eraser_button = ui.Button(renderer, button_0_patch, button_0_pressed_patch,
                              button_font, "Eraser", 4, WHITE, eraser_button_press)
    eraser_button.texture = eraser_icon
    eraser_button.posy += eyedropper_button.posy + \
        eyedropper_button.transform.height
    
    def fill_button_press():
        global brush_type 
        brush_type = BrushType.FILL
    fill_button = ui.Button(renderer, button_0_patch, button_0_pressed_patch, button_font, "Fill", 4, WHITE, fill_button_press)
    fill_button.texture = bucket_fill_icon
    fill_button.posy += eraser_button.posy + eraser_button.transform.height

    buttons = [pencil_button, eyedropper_button, eraser_button, fill_button]

    # editor grid
    grid = grid.Grid(renderer, Color(255, 255, 255, 255), 16, window.size)
    brush_tile_id = 1

    # load default tilemap
    level_name = "level_00"
    tilemap_filename = assets_dir + "/levels/" + level_name
    tilemap = Tilemap.from_file(tilemap_filename, assets_dir + "tilesets/",
                                renderer)

    # editor main loop
    lastTime = time.time()
    while True:
        # calculate the delta time
        currentTime = time.time()
        deltaTime: float = (currentTime - lastTime) * 1000  # time in ms
        lastTime: float = currentTime

        mouse_pos = pygame.mouse.get_pos()
        # inverse of the camera.transform method
        current_world_space_pos = Vector2(((mouse_pos[0] - half_screen_size[0]) / camera.scale) + camera.position.x,
                                          ((mouse_pos[1] - half_screen_size[1]) / camera.scale) + camera.position.y)
        current_tilemap_pos = Vector2(current_world_space_pos.x // tilemap.spriteset.tile_width,
                                      current_world_space_pos.y // tilemap.spriteset.tile_height)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEWHEEL:
                camera.on_scroll(event.x, event.y)
            elif event.type == KEYDOWN:
                if event.key == K_s:
                    if (event.mod & KMOD_CTRL):
                        print("Saving tilemap")
                        tilemap.save(tilemap_filename)
                        level_filename = level_name + ".json"
                        # pygame._sdl2.video.messagebox("Saved!", f"Successfully saved: {level_filename}", info=True)
                        print(f"Successfully saved: {level_filename}")
                elif event.key == K_r:
                    if brush_tile_id < tilemap.spriteset.get_max_tile_id():
                        brush_tile_id += 1
                elif event.key == K_e:
                    if brush_tile_id > 0:
                        brush_tile_id -= 1
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        (left_button, middle_button,
         right_button) = pygame.mouse.get_pressed(num_buttons=3)

        if left_button:
            # first check any buttons
            press_handled = False
            for index in range(len(buttons)):
                if buttons[index].transform.collidepoint(pygame.mouse.get_pos()):
                    buttons[index].handle_press()
                    press_handled = True
                    break
            if not press_handled:
                # then use the brush
                if brush_type == BrushType.PENCIL:
                    # keep the cursor within bounds
                    if current_tilemap_pos.x >= 0 and current_tilemap_pos.y >= 0:
                        tilemap.set_tile(int(current_tilemap_pos.x), int(
                            current_tilemap_pos.y), brush_tile_id)
                elif brush_type == BrushType.EYEDROPPER:
                    # keep the cursor within bounds
                    if current_tilemap_pos.x >= 0 and current_tilemap_pos.y >= 0:
                        new_tile_id = tilemap.get_tile(
                            int(current_tilemap_pos.x), int(current_tilemap_pos.y))
                        if new_tile_id > -1:
                            brush_tile_id = new_tile_id
                elif brush_type == BrushType.ERASER:
                    # keep the cursor within bounds
                    if current_tilemap_pos.x >= 0 and current_tilemap_pos.y >= 0:
                        # -1 is empty space
                        tilemap.set_tile(int(current_tilemap_pos.x),
                                     int(current_tilemap_pos.y), -1)
                elif brush_type == BrushType.FILL:
                    # flood fill
                    # keep cursor within bounds
                    if current_tilemap_pos.x >= 0 and current_tilemap_pos.y >= 0:
                        flood_fill(int(current_tilemap_pos.x), int(current_tilemap_pos.y), tilemap, tilemap.get_tile(int(current_tilemap_pos.x), int(current_tilemap_pos.y)), brush_tile_id)
        # tick
        camera.update(deltaTime)
        for button in buttons:
            button.update()

        # render
        renderer.draw_color = CLEAR_COLOR
        renderer.clear()

        # render tilemap
        tilemap.render(camera)

        # draw brush
        # keep the cursor within bounds
        if current_tilemap_pos.x >= 0 and current_tilemap_pos.y >= 0:
            # the rectangle of the current brush position (i.e. the selected tile)
            brush_rect = Rect((((current_tilemap_pos.x * tilemap.spriteset.tile_width) - camera.position.x) * camera.scale) + half_screen_size[0], ((
                (current_tilemap_pos.y * tilemap.spriteset.tile_height) - camera.position.y) * camera.scale) + half_screen_size[1], tilemap.spriteset.tile_width * camera.scale, tilemap.spriteset.tile_height * camera.scale)
            if brush_type == BrushType.PENCIL:
                # draw tile transparent
                tilemap.spriteset.draw(brush_tile_id, brush_rect, 100)
            elif brush_type == BrushType.EYEDROPPER:
                eyedropper_icon.draw(dstrect=brush_rect)
            elif brush_type == BrushType.ERASER:
                eraser_icon.draw(dstrect=brush_rect)
            elif brush_type == BrushType.FILL:
                bucket_fill_icon.draw(dstrect=brush_rect)

        # grid overlay
        grid.render(camera)

        # draw ui

        tile_pos_texture = Texture.from_surface(renderer, info_font.render(
            f"Mouse Pos: ({mouse_pos[0]}, {mouse_pos[1]}) Tile Pos: {int(current_tilemap_pos.x)}, {int(current_tilemap_pos.y)}, Tile ID = {brush_tile_id}", True, WHITE, BLACK))
        tile_pos_texture.draw(dstrect=tile_pos_texture.get_rect())

        # camera pos ui
        cam_pos_texture = Texture.from_surface(renderer, info_font.render(
            f"Camera Pos: ({camera.position.x}, {camera.position.y}) Camera Scale: {camera.scale}", True, WHITE, BLACK))
        cam_pos_texture.draw(dstrect=cam_pos_texture.get_rect().move(0, 20))

        # draw buttons
        for button in buttons:
            button.render()

        renderer.present()
