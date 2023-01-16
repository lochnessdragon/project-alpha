from enum import Enum

import pygame
from pygame._sdl2.video import Renderer, Texture
from pygame.locals import *
from physics import PhysicsCollider
from tilemap import Tilemap
from animation import TileAnimation
import camera
import utils
from spriteset import SpriteSet
from input import Input

"""
Represents a basic "unit" of the game.
Base class for the player, enemys, platforms, etc. etc.
"""
class Entity:
    def __init__(self, renderer: Renderer, sprite_sheet: SpriteSet):
        self.renderer = renderer
        self.sprite_sheet = sprite_sheet
        self.sprite_id = 0
        self.transform = Rect(0, 0, self.sprite_sheet.tile_width, self.sprite_sheet.tile_height)
        self.flipX = False
        self.flipY = False
        self.origin = (0, 0)
        self.angle = 0
        self.collider = PhysicsCollider(self);

    def update(self, deltaTime: float, tilemap: Tilemap):
        """
        update: updates the entity's physics
        """
        # update physics
        self.collider.update(deltaTime, tilemap)

    def render(self, camera):
        """
        render: draws the entity to the screen
        """
        if self.collider.draw:
            self.renderer.draw_color = Color(255, 0, 0, 255)
            self.renderer.draw_rect(camera.transform(self.transform))
        self.sprite_sheet.draw(self.sprite_id, camera.transform(self.transform), angle=self.angle, origin=self.origin, flipX=self.flipX, flipY=self.flipY)

class PlayerUpdate(Enum):
    NONE = 0
    DIED = 1
    WON = 2 # has the player reached the end goal

class Player(Entity):
    def __init__(self, renderer: Renderer, assets_dir: str, tilemap: Tilemap, start_pos: pygame.Vector2):
        super().__init__(renderer, SpriteSet(renderer, assets_dir + "img/spritesheet/explorer_sheet.png", 16, 16))
        # set start position
        self.transform.x = start_pos.x
        self.transform.y = start_pos.y

        # physics vars
        self.speed = 5
        self.max_speed = 20
        self.jump_force = 17
        self.friction = 0.05

        # bounds vars
        self.min_x = 0
        self.max_x = (tilemap._width * tilemap.spriteset.tile_width) - self.transform.width
        self.max_y = (tilemap._height * tilemap.spriteset.tile_height) - self.transform.height

        # animations
        self.idle_animation = TileAnimation(0, 3, 400) # breathing
        self.walk_animation = TileAnimation(4, 11, 100) # running
        self.jump_animation = TileAnimation(12, 14, 250) # jumping
        self.current_animation = self.idle_animation

        # sounds
        #self.walk_sound
        self.jump_sound = pygame.mixer.Sound(assets_dir + "audio/jump.wav")
        self.coin_sound = pygame.mixer.Sound(assets_dir + "audio/pickup.wav")
        self.death_sound = pygame.mixer.Sound(assets_dir + "audio/death.wav")

    def update(self, deltaTime: float, tilemap: Tilemap) -> (int, PlayerUpdate):
        """
        player update method, returns a tuple containing the score addition (for coins collected) and a PlayerUpdate enum value
        """
        super().update(deltaTime, tilemap)
        update_value = PlayerUpdate.NONE
        additional_score = 0 # keeps track of coin pickups

        adjTime = deltaTime / 10
        # react to keys pressed
        pressed_keys = pygame.key.get_pressed()
        
        move_axis = Input.get_move()
        self.collider.velocity.x += move_axis * self.speed * adjTime
        self.collider.velocity.x = max(-self.max_speed,  self.collider.velocity.x)
        self.collider.velocity.x = min(self.max_speed,  self.collider.velocity.x)
        
        if Input.get_jump():
            if self.collider.grounded:
                self.collider.velocity.y -= self.jump_force # up is negative (yes, its confusing)
                self.jump_sound.play()

        # update animation
        if not self.collider.grounded:
            if self.current_animation != self.jump_animation:
                self.current_animation.reset()
                self.current_animation = self.jump_animation
        elif abs(self.collider.velocity.x) > 0:
            if self.current_animation != self.walk_animation:
                self.current_animation.reset()
                self.current_animation = self.walk_animation
        else:
            if self.current_animation != self.idle_animation:
                self.current_animation.reset()
                self.current_animation = self.idle_animation

        self.sprite_id = self.current_animation.update(deltaTime, self)

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
            update_value = PlayerUpdate.DIED# fallen through floor
            self.death_sound.play()

        # check important tiles (goal, coins, deadly tiles)
        # transform the player's coordinates to tilemap coords
        tilemap_x_coord: int = int((self.transform.centerx - \
                         tilemap.position.x) // tilemap.spriteset.tile_width)
        tilemap_y_coord: int = int((self.transform.centery - \
                         tilemap.position.y) // tilemap.spriteset.tile_height)
        # check 3x3 cube centered on player for deadly tiles, coins or the goal
        for y in range(-1, 2):
            for x in range(-1, 2):
                tilemap_x_adj = tilemap_x_coord + x
                tilemap_y_adj = tilemap_y_coord + y
                try:
                    # check collision
                    tile_rect=Rect((tilemap_x_adj * tilemap.spriteset.tile_width) + tilemap.position.x, (tilemap_y_adj * tilemap.spriteset.tile_height) + tilemap.position.y, tilemap.spriteset.tile_width, tilemap.spriteset.tile_height)
                    # check for the players collision
                    if self.transform.colliderect(tile_rect):
                        tile_id = tilemap.get_tile(tilemap_x_adj, tilemap_y_adj)
                        if tile_id in tilemap.spriteset.deadly_tiles: # spikes
                            update_value = PlayerUpdate.DIED
                            self.death_sound.play()
                        if tile_id in tilemap.spriteset.score_tiles: # score
                            tilemap.set_tile(tilemap_x_adj, tilemap_y_adj, -1) # clear tile
                            additional_score += 100 # 100 per coin
                            self.coin_sound.play()
                        if tile_id == tilemap.spriteset.goal_tile: # win!
                            update_value = PlayerUpdate.WON
                except:
                    continue

        return (additional_score, update_value)

# testing entity
class TestBall(Entity):
    def __init__(self, renderer: Renderer, assets_dir: str):
        super().__init__(renderer, assets_dir + "img/ball.png")
        self.transform.width = 32
        self.transform.height = 32
        self.collider.velocity.y = 1

    def update(self, deltaTime: float):
        super().update(deltaTime)
