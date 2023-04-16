import pygame as pg
from settings import *


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, groups, surface=pg.Surface((16, 16))):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -8)


class Door(Tile):
    def __init__(self, pos, groups, surface=pg.Surface((16, 16))):
        super().__init__(pos, groups, surface)
        self.door_name = None

    def set_door_name(self, door_name):
        self.door_name = door_name
