import pygame as pg
from settings import *
import helper


class Dialogue:
    def __init__(self):
        self.font = pg.font.Font('imgs/BreatheFireIii-PKLOB.ttf', 24)
        self.display_surface = pg.display.get_surface()
        self.speed = 3
        self.counter = 0
        self.done = False
        self.image = pg.image.load("imgs/Retro_Textbox_01-A_Transparent.png")
        self.dialogue_image = pg.transform.scale(self.image, (640, 140))
        self.dialogue_rect = self.dialogue_image.get_rect(
            center=(640, 650))
        self.snip = self.font.render('', True, 'white')
        self.active_message = 0
        self.current_message = ""
        self.total_message = 0

    def intro_message(self):
        self.import_message(["Welcome knight, here is the last paradise", "The door on the left leads you to the merchant", "You can upgrade yourself using exp", "The door on the right leads you to the dungeon",
                             "You can defeat monsters  gain exp", "The final room on top leads you to the boss", "You must defeat 4 waves of monsters to enter the room", "Please save us from those monsters!"])

    def merchant_message(self):
        self.import_message(
            ["Welcome to my shop, what do you need?"])

    def boss_message(self):
        self.import_message(["I have been waiting for you"])

    def unreached_requirement_message(self):
        self.import_message(
            ["You have to defeat at least 4 waves of monsters!"])

    def import_message(self, message):
        self.active_message = 0
        self.done = False
        self.message = message
        self.total_message = len(message)
        self.counter = 0

    def display_dialogue(self):
        if self.active_message < self.total_message and not self.done:
            self.current_message = self.message[self.active_message]
            self.display_surface.blit(self.dialogue_image, self.dialogue_rect)
            if self.counter < self.speed * len(self.current_message):
                self.counter += 1
            elif self.counter >= self.speed*len(self.current_message):
                pass

            self.snip = self.font.render(
                self.current_message[0:self.counter//self.speed], True, 'white')
            self.display_surface.blit(self.snip, (380, 615))

    def next_dialogue(self):
        self.active_message += 1
        self.done = False
        self.counter = 0

    def clear_dialogue(self):
        self.done = True
