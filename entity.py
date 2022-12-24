import pygame
from pygame._sdl2.video import Renderer, Texture
from pygame.locals import *
from physics import PhysicsCollider
from tilemap import Tilemap
import camera
import utils

"""
Represents a basic "unit" of the game.
Base class for the player, enemys, platforms, etc. etc.
"""
class Entity:
    def __init__(self, renderer: Renderer, texture_filename: Texture):
        self.renderer = renderer
        self.texture = Texture.from_surface(renderer, pygame.image.load(texture_filename))
        self.transform = self.texture.get_rect()
        self.flipX = False
        self.flipY = False
        self.origin = (0, 0)
        self.angle = 0
        self.collider = PhysicsCollider(self);

    def update(self, deltaTime: float, tilemap: Tilemap):
        # update physics
        self.collider.update(deltaTime, tilemap)

    def render(self, camera):
        if self.collider.draw:
            self.renderer.draw_color = Color(255, 0, 0, 255)
            self.renderer.draw_rect(camera.transform(self.transform))
        self.texture.draw(dstrect = camera.transform(self.transform), angle=self.angle, origin=self.origin, flipX=self.flipX, flipY=self.flipY)

class Player(Entity):
    def __init__(self, renderer: Renderer, assets_dir: str, tilemap: Tilemap):
        super().__init__(renderer, assets_dir + "img/player.png")
        self.transform.y = 16 * 6
        self.speed = 5
        self.max_speed = 20
        self.jump_force = 15
        self.friction = 0.05
        self.min_x = 0
        self.max_x = (tilemap._width * tilemap.spriteset.tile_width) - self.transform.width
        self.max_y = (tilemap._height * tilemap.spriteset.tile_height) - self.transform.height

    def update(self, deltaTime: float, tilemap: Tilemap) -> bool:
        """
        player update method, returns true if the player has died (i.e. should reset the level)
        """
        super().update(deltaTime, tilemap)
        adjTime = deltaTime / 10
        # react to keys pressed
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.collider.velocity.x -= self.speed
            self.collider.velocity.x = max(-self.max_speed,  self.collider.velocity.x)
        if pressed_keys[K_RIGHT]:
            self.collider.velocity.x += self.speed
            self.collider.velocity.x = min(self.max_speed,  self.collider.velocity.x)
        if pressed_keys[K_UP]:
            if self.collider.grounded:
                self.collider.velocity.y -= self.jump_force # up is negative (yes, its confusing)

        # flip player
        if self.collider.velocity.x < 0:
            self.flipX = True
        elif self.collider.velocity.x > 0:
            self.flipX = False

        # dampen velocity
        if abs(self.collider.velocity.x) > 0:
            self.collider.velocity.x = utils.sign(self.collider.velocity.x) * max(0, (abs(self.collider.velocity.x) - (self.friction * deltaTime)))

        # keep the player within bounds
        self.transform.x = max(self.min_x, self.transform.x)
        self.transform.x = min(self.max_x, self.transform.x)

        # check lose conditions
        if self.transform.y > self.max_y:
            return True # fallen through floor

        # check deadly tiles
        # transform the player's coordinates to tilemap coords
        tilemap_x_coord: int = int((self.transform.centerx - \
                         tilemap.position.x) // tilemap.spriteset.tile_width)
        tilemap_y_coord: int = int((self.transform.centery - \
                         tilemap.position.y) // tilemap.spriteset.tile_height)
        # check 3x3 cube centered on player
        for y in range(-1, 2):
            for x in range(-1, 2):
                tilemap_x_adj = tilemap_x_coord + x
                tilemap_y_adj = tilemap_y_coord + y
                try:
                    if tilemap.is_deadly(tilemap_x_adj, tilemap_y_adj):
                        # check collision
                        tile_rect=Rect((tilemap_x_adj * tilemap.spriteset.tile_width) + tilemap.position.x, (tilemap_y_adj * tilemap.spriteset.tile_height) + tilemap.position.y, tilemap.spriteset.tile_width, tilemap.spriteset.tile_height)
                        # check for the players collision
                        if self.transform.colliderect(tile_rect):
                            return True
                except:
                    continue

class TestBall(Entity):
    def __init__(self, renderer: Renderer, assets_dir: str):
        super().__init__(renderer, assets_dir + "img/ball.png")
        self.transform.width = 32
        self.transform.height = 32
        self.collider.velocity.y = 1

    def update(self, deltaTime: float):
        super().update(deltaTime)
