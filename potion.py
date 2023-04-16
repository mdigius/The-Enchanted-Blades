import pygame as pg
import item
from settings import *
import helper

# Potion class extends item

class Potion(item):
    def __init__(self, groups, itemID, itemName, itemDescription, itemImage, potionType, healingAmount):
        super().__init__(groups, itemID, itemName, itemDescription, itemImage)
        self.potionType = potionType
        self.healingAmount = healingAmount
