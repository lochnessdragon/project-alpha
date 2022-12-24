import pygame
from pygame import Vector2
from pygame.locals import *
from tilemap import Tilemap
from utils import sign

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
        self.grounded = False
        self.draw = False

    def update(self, deltaTime: float, tilemap: Tilemap):
        adjTime = deltaTime / 100
        if not self.is_static:
            # reset grounded state
            self.grounded = False

            # commonly used equations
            tile_size = Vector2(tilemap.spriteset.tile_width, tilemap.spriteset.tile_height)

            # check if the movement will impact with the tilemap, and if so, clear out velocity and snap player position

            # transform the player's coordinates to tilemap coords
            tilemap_x_coord: int = int((self.entity.transform.centerx - \
                             tilemap.position.x) // tile_size.x)
            tilemap_y_coord: int = int((self.entity.transform.centery - \
                             tilemap.position.y) // tile_size.y)
            # print(f"Player located at: ({tilemap_x_coord}, {tilemap_y_coord})")

            # test collider
            player_rect_test_x = self.entity.transform.move(self.velocity.x * adjTime, 0)
            player_rect_test_y = self.entity.transform.move(0, self.velocity.y * adjTime)

            # check for collisions on the y axis
            # positive is down
            velocity_y_sign=sign(self.velocity.y)
            if velocity_y_sign != 0:
                tilemap_y_adj=tilemap_y_coord + velocity_y_sign

                for x in range(-1, 2):
                    tilemap_x_adj = tilemap_x_coord + x
                    try:
                        if tilemap.is_solid(tilemap_x_adj, tilemap_y_adj):
                            # check collision
                            tile_rect=Rect((tilemap_x_adj * tile_size.x) + tilemap.position.x, (tilemap_y_adj * tile_size.y) + tilemap.position.y, tile_size.x, tile_size.y)
                            # check for the players collision
                            if player_rect_test_y.colliderect(tile_rect):
                                # set the player's y position to be right on top of the block
                                if velocity_y_sign > 0: # i.e. we hit the block on our bottom
                                    self.entity.transform.y = tile_rect.y - self.entity.transform.height
                                else: # we hit the block on our top
                                    self.entity.transform.y = tile_rect.y + tile_rect.height - 1
                                self.velocity.y = 0
                    except:
                        continue

            # check if the player is grounded
            try:
                y_mod = self.entity.transform.y % tile_size.y
                close_to_ground = y_mod < (tile_size.y / 4) # arbitrary check to see if the player is within a few pixels of the ground
                if tilemap.is_solid(tilemap_x_coord, tilemap_y_coord + 1) and close_to_ground:
                    self.grounded = True
            except:
                pass # required here to prevent syntax error

            # check for collisions on the x axis
            velocity_x_sign = sign(self.velocity.x)
            if velocity_x_sign != 0:
                tilemap_x_adj = tilemap_x_coord + velocity_x_sign

                for y in range(-1, 2):
                    tilemap_y_adj = tilemap_y_coord + y
                    try:
                        if tilemap.is_solid(tilemap_x_adj, tilemap_y_adj):
                            # check collision
                            tile_rect=Rect((tilemap_x_adj * tile_size.x) + tilemap.position.x, (tilemap_y_adj * tile_size.y) + tilemap.position.y, tile_size.x, tile_size.y)
                            # print(tile_rect)
                            if player_rect_test_x.colliderect(tile_rect):
                                # set the player's x position to be right next to the block
                                if velocity_x_sign > 0: # i.e. we hit the block on our right
                                    self.entity.transform.x = tile_rect.x - self.entity.transform.width
                                else: # we hit the block on our left
                                    self.entity.transform.x = tile_rect.x + tile_rect.width - 1
                                self.velocity.x=0
                    except:
                        continue

            # update movement
            self.entity.transform.x += self.velocity.x * adjTime
            self.entity.transform.y += self.velocity.y * adjTime
            self.velocity.x += self.acceleration.x * adjTime
            self.velocity.y += self.acceleration.y * adjTime

            # if the collider is not grounded, apply gravity
            if not self.grounded:
                self.acceleration.y=self.gravity
