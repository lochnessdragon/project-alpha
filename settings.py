from enum import Enum

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

class Settings:
    # def __init__(self):
    #     self.deserialize()

    def add_setting(self, name: str, default_value, type):
        self.name = default_value

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
    settings.add_setting("keymaps.move_left", TOMLType.INTEGER, K_LEFT)
    settings.deserialize()
    print(settings.keymaps.move_left)