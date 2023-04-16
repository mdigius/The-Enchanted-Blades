import pygame as pg
import item
from settings import *
import helper

# equipment class extends item
# armor, artifacts, etc.

class Equipment(item):
    def __init__(self, groups, itemID, itemName, itemDescription, itemImage, equipmentType, equipmentSlot, attackBonus, defenseBonus):
        super().__init__(groups, itemID, itemName, itemDescription, itemImage)
        self.equipmentType = equipmentType
        self.equipmentSlot = equipmentSlot
        self.attackBonus = attackBonus
        self.defenseBonus = defenseBonus

