import pygame as pg
import item
from settings import *
import helper

# weapon class inherit item

class Weapon(item):
    def __init__(self, groups, itemID, itemName, itemDescription, itemImage, weaponType, attackDamage, attackRange, durability):
        super().__init__(groups, itemID, itemName, itemDescription, itemImage)
        self.weaponType = weaponType
        self.attackDamage = attackDamage
        self.attackRange = attackRange
        self.durability = durability

    def reduceDurability(self, damage):
        self.durability -= damage