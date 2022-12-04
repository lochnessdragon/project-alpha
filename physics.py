import pygame
from pygame import Vector2
from pygame.locals import *
from tilemap import Tilemap

# from entity import Entity

"""
PhysicsCollider: represents any physical body in the physics world, it will update the objects transform
and handle all body interactions between the object and other objects.
"""
class PhysicsCollider:
    def __init__(self, entity):
        self.is_static = False
        self.gravity = 9.8
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.entity = entity

    def update(self, deltaTime: float, tilemap: Tilemap):
        if not self.is_static:
            # check if the movement will impact with the tilemap, and if so, clear out velocity and snap player position
            
            # transform the player's coordinates to tilemap coords
            tilemap_x_coord = (self.entity.x - tilemap.x) // tilemap.tile_width
            tilemap_y_coord = (self.entity.y - tilemap.y) // tilemap.tile_height

            # update movement
            self.entity.transform.x += self.velocity.x * deltaTime
            self.entity.transform.y += self.velocity.y * deltaTime
            self.velocity.x += self.acceleration.x * deltaTime
            self.velocity.y += self.acceleration.y * deltaTime

            # if there are no collisions on the bottom, apply gravity
            self.acceleration.y = self.gravity