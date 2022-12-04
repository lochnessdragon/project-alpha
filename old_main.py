import sys
import math

import pygame
from pygame.locals import *
from pygame._sdl2.video import Window, Renderer

def inverse(x: int):
    if x == 1:
        return 0
    elif x == 0:
        return 1

BG = Color(100, 100, 100, 255)
ON = Color(160, 160, 80, 255)
OFF = Color(0, 0, 0, 255)
circle_radius = 50

window = Window("Project 1.2.5")
renderer = Renderer(window, accelerated=1, vsync=True)

buttons = [[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0]]

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                # translate mouse x and y to button location
                print(f"Mouse clicked at: {event.pos[0]}, {event.pos[1]}")
                button_x = math.floor(event.pos[0] / (circle_radius + 5))
                button_y = math.floor(event.pos[1] / (circle_radius + 5))
                print(f"{button_x} {button_y}")
                if button_y < len(buttons) and button_x < len(buttons[0]):
                    buttons[button_y][button_x] = inverse(buttons[button_y][button_x])
                    if button_y + 1 < len(buttons):
                        buttons[button_y + 1][button_x] = inverse(buttons[button_y + 1][button_x])
                    if button_y - 1 >= 0:
                        buttons[button_y - 1][button_x] = inverse(buttons[button_y - 1][button_x])
                    if button_x + 1 < len(buttons[0]):
                        buttons[button_y][button_x + 1] = inverse(buttons[button_y][button_x + 1])
                    if button_x - 1 >= 0:
                        buttons[button_y][button_x - 1] = inverse(buttons[button_y][button_x - 1])


    renderer.draw_color = BG
    renderer.clear()

    for y in range(len(buttons)):
        for x in range(len(buttons[y])):
            if buttons[y][x] == 0:
                renderer.draw_color = OFF
            elif buttons[y][x] == 1:
                renderer.draw_color = ON
            renderer.fill_rect(Rect(x * (circle_radius + 5), y * (circle_radius + 5), circle_radius, circle_radius))

    renderer.present()