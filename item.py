import pygame as pg
from settings import *
import helper

# item class

class Item(pg.sprite.Sprite):
    def __init__(self, groups, itemID, itemName, xPos, yPos):
        super().__init__(groups)
        self.itemID = itemID
        self.itemName = itemName
        self.itemDescription = "itemDescription"
        self.itemImage = pg.image.load('imgs/items/apple.png')
        self.xPos = xPos
        self.yPos = yPos

    def setX(self, xPos):
        self.xPos = xPos
    
    def setY(self, yPos):
        self.yPos = yPos


