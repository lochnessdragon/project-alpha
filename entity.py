import pygame 
from pygame._sdl2.video import Renderer, Texture
from pygame.locals import *
from physics import PhysicsCollider
from tilemap import Tilemap

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
    
    def render(self):
        if self.collider.draw:
            self.renderer.draw_color = Color(255, 0, 0, 255)
            self.renderer.draw_rect(self.transform)
        self.texture.draw(dstrect = self.transform, angle=self.angle, origin=self.origin, flipX=self.flipX, flipY=self.flipY)

class Player(Entity):
    def __init__(self, renderer: Renderer, assets_dir: str):
        super().__init__(renderer, assets_dir + "/img/player.png")
        self.transform.width = 64
        self.transform.height = 64
        self.transform.y = 64 * 3
        #self.collider.draw = True
        self.speed = 5
        self.max_speed = 25
        self.jump_force = 40
    
    def update(self, deltaTime: float, tilemap: Tilemap):
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
        #self.collider.velocity.x = self.collider.velocity.x

class TestBall(Entity):
    def __init__(self, renderer: Renderer, assets_dir: str):
        super().__init__(renderer, assets_dir + "/img/ball.png")
        self.transform.width = 32
        self.transform.height = 32
        self.collider.velocity.y = 1
    
    def update(self, deltaTime: float):
        super().update(deltaTime)