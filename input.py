from enum import Enum

import pygame
import pygame._sdl2.controller
from pygame.locals import *

class ActiveInputSource:
	KEYBOARD = 0
	CONTROLLER = 1

class Input:
	controllers = []
	keys = [] 
	
	def update():
		Input.keys = pygame.key.get_pressed()
	
	def get_jump():
		value = False
		if Input.keys[K_UP] or Input.keys[K_w] or Input.keys[K_SPACE]:
			value = True 
		if len(Input.controllers) > 0:
			current_controller = Input.controllers[0]
			if current_controller.get_button(CONTROLLER_BUTTON_A) or current_controller.get_button(CONTROLLER_BUTTON_DPAD_UP):
				value = True
		return value
		
	def get_move():
		value = 0
		if Input.keys[K_LEFT] or Input.keys[K_a]:
			value = -1
		if Input.keys[K_RIGHT] or Input.keys[K_d]:
			value = 1
		if len(Input.controllers) > 0:
			current_controller = Input.controllers[0]
			if current_controller.get_button(CONTROLLER_BUTTON_DPAD_LEFT):
				value = -1
			if current_controller.get_button(CONTROLLER_BUTTON_DPAD_RIGHT):
				value = 1
			axis_value = current_controller.get_axis(CONTROLLER_AXIS_LEFTX)
			if abs(axis_value) > 10000:
				value = axis_value / 32768 # max controller value
		return value
	
	def init():
		print("Input information:")
		pygame._sdl2.controller.init()
		for index in range(pygame._sdl2.controller.get_count()):
			print(f"Controller {index}: {pygame._sdl2.controller.name_forindex(index)}")
			Input.controllers.append(pygame._sdl2.controller.Controller(index))
