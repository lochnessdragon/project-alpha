import json

import pygame
from pygame.locals import *
from pygame._sdl2.video import Renderer, Texture


class SpriteSet(object):
    """
    SpriteSet: represents a source texture that is tiled, from which multiple sprites can be renderered
    It's tied to a renderer, and conversly, a window
    """

    def __init__(self, renderer: Renderer, filename: str, tile_width: int,
                 tile_height: int):
        self.texture = Texture.from_surface(renderer,
                                            pygame.image.load(filename))

        if self.texture.width % tile_width != 0:
            raise ValueError(
                f"The width of: {filename} is not evenly divisible by the tile width of: {tile_width}"
            )
        if self.texture.height % tile_height != 0:
            raise ValueError(
                f"The height of: {filename} is not evenly divisible by the tile height of: {tile_height}"
            )

        self.tile_width = tile_width
        self.tile_height = tile_height
        self.tiles_per_row = int(self.texture.width / tile_width)
        self.tiles_per_col = int(self.texture.height / tile_height)
        self.solid_tiles = []
        self.deadly_tiles = []
        self.goal_tile = None
        self.score_tiles = []
        self._max_tile_id = self.tiles_per_row * self.tiles_per_col

        # create array of list of rects for use in the draw method (optimization)
        self._source_rects = []
        for id in range(self._max_tile_id + 1):
            tile_x = (id % self.tiles_per_row) * self.tile_width
            tile_y = (id // self.tiles_per_row) * self.tile_height
            tile_rect = Rect(tile_x, tile_y, self.tile_width, self.tile_height)
            self._source_rects.append(tile_rect)

    def get_max_tile_id(self) -> int:
        return self._max_tile_id

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
            return RuntimeError(
                f"JSON file: {json_filename} doesn't contain a tile_width key")
        if not "tile_height" in data.keys():
            return RuntimeError(
                f"JSON file: {json_filename} doesn't contain a tile_height key"
            )

        tile_width = data["tile_width"]
        tile_height = data["tile_height"]
        image_filename = filename + ".png"
        sprite_set = SpriteSet(renderer, image_filename, tile_width,
                               tile_height)

        if "solid" in data.keys():
            for id in data["solid"]:
                sprite_set.solid_tiles.append(id)

        if "deadly" in data.keys():
            for id in data["deadly"]:
                sprite_set.deadly_tiles.append(id)

        if "score_pickup" in data.keys():
            for id in data["score_pickup"]:
                sprite_set.score_tiles.append(id)

        if "goal" in data.keys():
            sprite_set.goal_tile = data["goal"]

        return sprite_set

    def draw(self, id: int, dest: Rect, alpha=255):
        """Renders a tile to the screen, given an id and a destination rectangle."""
        if id > self._max_tile_id:
            raise ValueError(
                f"Tile id: {id} is outside the range of this tileset<max={self._max_tile_id}>."
            )

        self.texture.alpha = alpha
        self.texture.draw(srcrect=self._source_rects[id], dstrect=dest)
