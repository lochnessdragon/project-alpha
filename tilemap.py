import json

import pygame
from pygame.locals import *
from pygame._sdl2.video import Renderer

from spriteset import SpriteSet


class Tilemap(object):
    """Tilemap: manages and displays tiles in a map."""

    def __init__(self, spriteset: SpriteSet, x: int, y: int, width: int, height: int):
        self.spriteset = spriteset
        self.position = pygame.Vector2(x, y)
        self.scale = 3  # temp variable until I get camera's implemented
        self._width = width
        self._height = height
        self.tiles = [[1 for x in range(width)] for x in range(height)]

    def set_tile(self, x: int, y: int, id: int):
        if x > self._width or y > self._height:
            raise ValueError("The X and Y provided are out of range.")
        self.tiles[y][x] = id

    def get_tile(self, x: int, y: int) -> int:
        if x > self._width or y > self._height:
            raise ValueError("The X and Y provided are out of range.")
        return self.tiles[y][x]
    
    def is_soild(self, x: int, y: int) -> bool:
        return self.get_tile(x, y) in self.spriteset.solid_tiles

    @staticmethod
    def from_file(filename: str, tilemap_dir: str, renderer: Renderer):
        """Loads a tilemap from a .json file"""
        json_filename = filename + ".json"
        with open(json_filename) as file:
            data = json.load(file)

        if not "tilemap" in data.keys():
            raise ValueError(
                f"Tilemap file: {json_filename} doesn't contain the tilemap key.")
        if not "width" in data.keys():
            raise ValueError(
                f"Tilemap file: {json_filename} doesn't contain the width key.")
        if not "height" in data.keys():
            raise ValueError(
                f"Tilemap file: {json_filename} doesn't contain the height key.")
        if not "tiles" in data.keys():
            raise ValueError(
                f"Tilemap file: {json_filename} doesn't contain the tiles key.")

        tilemap_filename = tilemap_dir + data["tilemap"]
        map_width = data["width"]
        map_height = data["height"]

        # check if the tiles array actually contains the correct amount of tiles
        tiles_data_len = len(data["tiles"])
        if tiles_data_len != (map_width * map_height):
            raise ValueError(
                f"Tilemap file: {json_filename} doesn't contain the correct number of tiles. Expected: {map_width * map_height} Actual: {tiles_data_len}")

        sprite_set = SpriteSet.from_file(tilemap_filename, renderer)
        tilemap = Tilemap(sprite_set, 0, 0, map_width, map_height)

        # load tile ids into the map
        for y in range(map_height):
            for x in range(map_width):
                tilemap.set_tile(x, y, data["tiles"][(y * map_width) + x])

        return tilemap

    def render(self):
        """Renders the tilemap to the screen"""
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                rect = Rect(self.position.x + (x * self.spriteset.tile_width * self.scale), self.position.y + (
                    y * self.spriteset.tile_height * self.scale), self.scale * self.spriteset.tile_width, self.scale * self.spriteset.tile_height)
                self.spriteset.draw(self.tiles[y][x], rect)
