import json

import pygame
from pygame.locals import *
from pygame._sdl2.video import Renderer, Texture 

class SpriteSet(object):
    """
    SpriteSet: represents a source texture that is tiled, from which multiple sprites can be renderered
    It's tied to a renderer, and conversly, a window
    """

    def __init__(self, renderer: Renderer, filename: str, tile_width: int, tile_height: int):
        self.texture = Texture.from_surface(renderer, pygame.image.load(filename))

        if self.texture.width % tile_width != 0:
            raise ValueError(f"The width of: {filename} is not evenly divisible by the tile width of: {tile_width}")
        if self.texture.height % tile_height != 0:
            raise ValueError(f"The height of: {filename} is not evenly divisible by the tile height of: {tile_height}")

        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tiles_per_row = int(self.texture.width / tile_width)
        self.tiles_per_col = int(self.texture.height / tile_height)
        self.solid_tiles = []
        self._max_tile_id = self.tiles_per_row * self.tiles_per_col
    
    @staticmethod
    def from_file(filename: str, renderer: Renderer):
        """
        Loads a sprite set from a file, 
        filename references the prefix of the two files (.json and .png) that will describe the tilemap
        e.x. assets/tilemap will translate to assets/tilemap.json and assets/tilemap.png
        """
        json_filename = filename + ".json"
        with open(json_filename) as file:
            data = json.load(file)
        
        if not "tile_width" in data.keys():
            return RuntimeError(f"JSON file: {json_filename} doesn't contain a tile_width key")
        if not "tile_height" in data.keys():
            return RuntimeError(f"JSON file: {json_filename} doesn't contain a tile_height key")

        tile_width = data["tile_width"]
        tile_height = data["tile_height"]
        image_filename = filename + ".png"
        sprite_set = SpriteSet(renderer, image_filename, tile_width, tile_height)

        if "solid" in data.keys():
            for id in data["solid"]:
                sprite_set.solid_tiles.append(id)

        return sprite_set
    
    def draw(self, id: int, dest: Rect):
        """Renders a tile to the screen, given an id and a destination rectangle."""
        if id > self._max_tile_id:
            raise ValueError(f"Tile id: {id} is outside the range of this tileset<max={self._max_tile_id}>.")

        tile_x = (id % self.tiles_per_row) * self.tile_width
        tile_y = (id // self.tiles_per_row) * self.tile_height
        tile_rect = Rect(tile_x, tile_y, self.tile_width, self.tile_height)
        self.texture.draw(srcrect=tile_rect, dstrect=dest)