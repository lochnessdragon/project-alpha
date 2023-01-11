import json

import pygame
from pygame.locals import *
from pygame._sdl2.video import Renderer

from spriteset import SpriteSet
import camera


class Tilemap(object):
    """Tilemap: manages and displays tiles in a map."""

    def __init__(self, filename: str, spriteset: SpriteSet, tileset_name: str,
                 x: int, y: int, width: int, height: int):
        self.filename = filename
        self.spriteset = spriteset
        self.position = pygame.Vector2(x, y)
        self._width = width
        self._height = height
        self.tiles = [[1 for x in range(width)] for x in range(height)]
        self.tileset_name = tileset_name

    def set_tile(self, x: int, y: int, id: int):
        if x >= self._width:
            # increase the tilemap's range
            self._width += (x - (self._width - 1))
            for row in range(self._height):
                for col in range(self._width):
                    if col >= len(self.tiles[row]):
                        self.tiles[row].append(-1)  # add an air tile

        if y >= self._height:
            # increase the tilemap's range
            self._height += (y - (self._height - 1))
            for row in range(self._height):
                if row >= len(self.tiles):
                    self.tiles.append([-1 for col in range(self._width)
                                       ])  # add a bunch of air tiles
        self.tiles[y][x] = id

    def get_tile(self, x: int, y: int) -> int:
        if x >= self._width or y >= self._height or x < 0 or y < 0:
            raise ValueError("The X and Y provided are out of range.")
        return self.tiles[y][x]

    def is_solid(self, x: int, y: int) -> bool:
        return self.get_tile(x, y) in self.spriteset.solid_tiles

    def is_deadly(self, x: int, y: int) -> bool:
        return self.get_tile(x, y) in self.spriteset.deadly_tiles

    # serialization below
    # yes, I know I could have used Pickle, but I needed to load a texture in, and I don't think pickle can do that
    # idk tho
    @staticmethod
    def from_file(filename: str, tileset_dir: str, renderer: Renderer):
        """
        Loads a tilemap from a .json file
        Returns the the tilemap
        """
        json_filename = filename + ".json"
        with open(json_filename) as file:
            data = json.load(file)

        if not "tileset" in data.keys():
            raise ValueError(
                f"Tilemap file: {json_filename} doesn't contain the tileset key."
            )
        if not "width" in data.keys():
            raise ValueError(
                f"Tilemap file: {json_filename} doesn't contain the width key."
            )
        if not "height" in data.keys():
            raise ValueError(
                f"Tilemap file: {json_filename} doesn't contain the height key."
            )
        if not "tiles" in data.keys():
            raise ValueError(
                f"Tilemap file: {json_filename} doesn't contain the tiles key."
            )

        tileset_filename = tileset_dir + data["tileset"]
        map_width = data["width"]
        map_height = data["height"]

        # check if the tiles array actually contains the correct amount of tiles
        tiles_data_len = len(data["tiles"])
        if tiles_data_len != (map_width * map_height):
            raise ValueError(
                f"Tilemap file: {json_filename} doesn't contain the correct number of tiles. Expected: {map_width * map_height} Actual: {tiles_data_len}"
            )

        sprite_set = SpriteSet.from_file(tileset_filename, renderer)
        tilemap = Tilemap(json_filename, sprite_set, data["tileset"], 0, 0,
                          map_width, map_height)

        # load tile ids into the map
        for y in range(map_height):
            for x in range(map_width):
                tilemap.set_tile(x, y, data["tiles"][(y * map_width) + x])

        return tilemap

    def save(self, filename: str):
        """
        save - writes the tilemap to the file specified by the string
        filename: the file to write the tilemap to
        """

        json_filename = filename + ".json"

        tile_data = []
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                tile_data.append(self.tiles[y][x])

        json_data = {
            "tileset": self.tileset_name,
            "width": self._width,
            "height": self._height,
            "tiles": tile_data
        }

        with open(json_filename, "w") as file:
            json.dump(json_data, file, indent="\t")

    def reset(self):
        """
        Reloads the tiles in the map from the source file
        """
        with open(self.filename) as file:
            data = json.load(file)
        # reload tile ids into the map
        for y in range(self._height):
            for x in range(self._width):
                tile_id = data["tiles"][(y * self._width) + x]
                self.set_tile(x, y, tile_id)

    def render(self, camera):
        """Renders the tilemap to the screen"""
        # we should be able to skip tiles that are outside the screen (optimization)
        min_x = -camera._half_screen_size[0]  # furthest left pixel (x)
        # convert screen to world coordinates
        min_x /= camera.scale
        min_x += camera.position.x
        min_x /= self.spriteset.tile_width
        min_x = int(min_x)
        min_x = max(min_x, 0)

        max_x = camera._half_screen_size[0]  # furthest right pixel (x)
        # screen -> world (literally an inverse of the camera transform calculation)
        max_x /= camera.scale
        max_x += camera.position.x
        max_x /= self.spriteset.tile_width
        max_x = int(max_x)
        max_x = min(max_x + 1, self._width)

        # lets do this 2 more times!
        min_y = -camera._half_screen_size[1]
        min_y = int(((min_y / camera.scale) + camera.position.y) /
                    self.spriteset.tile_height)
        min_y = max(min_y, 0)

        max_y = int((
            (camera._half_screen_size[1] / camera.scale) + camera.position.y) /
                    self.spriteset.tile_height)
        max_y = min(max_y + 1, self._height)

        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                if self.tiles[y][x] != -1:  # ignore empty tiles
                    rect = Rect(
                        self.position.x + (x * self.spriteset.tile_width),
                        self.position.y + (y * self.spriteset.tile_height),
                        self.spriteset.tile_width, self.spriteset.tile_height)
                    self.spriteset.draw(self.tiles[y][x], camera.transform(rect))
