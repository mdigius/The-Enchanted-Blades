import pygame as pg
import item
from settings import *
import helper

# loot class extends item

class Loot(item):
    def __init__(self, groups, itemID, itemName, itemDescription, itemImage, lootType, value):
        super().__init__(groups, itemID, itemName, itemDescription, itemImage)
        self.lootType = lootType
        self.value = value
