import pygame
from pygame.locals import *
from pygame import Vector2
import entity

class Camera:
    """
    Displaces the world around it to simulate a moving camera.
    This is the base class for EditorCamera and PlayerCamera
    """

    def __init__(self, screen_size: (int, int)):
        self.speed = 1
        self.position = Vector2(0, 0) # this is the pixel that the center of the camera should be focused on.
        self.scale = 1  # 1:1 mapping of pixel to pixel. lower number is zoomed out, higher number is zoomed in
        self.screen_size = screen_size
        self._half_screen_size = (screen_size[0] // 2, screen_size[1] // 2)

    def update(self, deltaTime: float):
        """
        Update - an interface method that is used for camera movement
        """
        pass

    def transform(self, rect: Rect) -> Rect:
        """
        transform: moves the rect to the correct position based on the camera's information
        """
        # apply translation
        new_rect = rect.move(-self.position.x, -self.position.y)

        # apply scale (from center of the screen)
        new_rect.x *= self.scale
        new_rect.y *= self.scale
        new_rect.width *= self.scale
        new_rect.height *= self.scale

        # center within the screen
        new_rect.x += self._half_screen_size[0]
        new_rect.y += self._half_screen_size[1]

        return new_rect


class EditorCamera(Camera):
    """
    The Camera class that the editor uses
    """

    def __init__(self, screen_size: (int, int)):
        super().__init__(screen_size)
        self.min_zoom = 0.5
        self.max_zoom = 4
        self.zoom_speed = 0.25


    def update(self, deltaTime: float):
        time_in_ds = deltaTime / 10
        # handle movement events
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            # move left
            self.position.x -= self.speed * time_in_ds
        if keys[K_RIGHT] or keys[K_d]:
            # move right
            self.position.x += self.speed * time_in_ds
        if keys[K_UP] or keys[K_w]:
            # move up
            self.position.y -= self.speed * time_in_ds
        if keys[K_DOWN] or keys[K_s]:
            # check for ctrl+s
            if not keys[K_LCTRL] and not keys[K_RCTRL]:
                # move down
                self.position.y += self.speed * time_in_ds

    def on_scroll(self, x: float, y: float):
        """
        on_scroll: react to scroll events by zooming in the camera
        """
        # print(f"{x}, {y}")

        # used so that we can center the zoom on the point the user is at (not implemented yet)
        mouse_position = pygame.mouse.get_pos()
        # positive y is zoom in, negative is zoom out
        self.scale += y * self.zoom_speed

        # cap zoom
        self.scale = max(self.scale, self.min_zoom)
        self.scale = min(self.scale, self.max_zoom)


class PlayerCamera(Camera):
    """
    A basic follow camera for the player.
    """

    def __init__(self, screen_size: (int, int), player, tilemap):
        super().__init__(screen_size)
        self.follow_entity = player
        self.scale = 2 # simply setting the scale to something reasonably zoomed in
        self.min_x = 0
        self.max_x = tilemap._width * tilemap.spriteset.tile_width
        self.max_y = tilemap._height * tilemap.spriteset.tile_height

    def update(self, deltaTime: float):
        """
        A method to simply follow the player around
        """
        if self.position.x != self.follow_entity.transform.centerx:
            self.position.x = self.follow_entity.transform.centerx
        if self.position.y != self.follow_entity.transform.centery:
            self.position.y = self.follow_entity.transform.centery

        # cap the x and y positions
        self.position.x = max(self.position.x, self.min_x + (self._half_screen_size[0] // self.scale))
        self.position.x = min(self.position.x, self.max_x - (self._half_screen_size[0] // self.scale))
        self.position.y = min(self.position.y, self.max_y - (self._half_screen_size[1] // self.scale))
