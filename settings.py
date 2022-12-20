from enum import Enum
import types

import tomli
import tomli_w
from pygame.locals import *

class TOMLType(Enum):
    STRING = 1
    INTEGER = 2
    FLOAT = 3
    BOOL = 4
    DATE = 5
    TIME = 6
    DATETIME = 7
    ARRAY = 8
    TABLE = 9

'''
Represents either one setting or a group of settings for a tree like fashion
'''
class Settings:
    def __init__(self, name=None, desc, type=TOMLType.TABLE, default_value=None):
        ''''''
        self.deserialize()

    def add_setting(self, name: str, desc: str, default_value, type):
        parts = name.split(".")
        for part in parts:
            print(part)
        self.__dict__[name] = default_value
        # self["keymaps"]["move_left"]


    def restore_defaults():
        # set default values

        # write to disk
        serialize()

    def deserialize(self):
        try:
            with open("settings.toml", "rb") as f:
                data = tomli.load(f)
                print(data)
        except:
            print("Invalid settings.toml file")
            self.restore_defaults()
        return

    def serialize(self):

        return

if __name__ == "__main__":
    settings = Settings()
    settings.add_setting("keymaps.move_left", "Key binding to move left", TOMLType.INTEGER, K_LEFT)
    # settings.deserialize()
    print(settings.keymaps.move_left)
