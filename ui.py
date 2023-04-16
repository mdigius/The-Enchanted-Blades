import pygame
import pygame as pg
import sys
import map
from player import *
from settings import *
from sounds import Sounds


class UI:
    def __init__(self):
        # general
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.Font('imgs/BreatheFireIii-PKLOB.ttf', 20)

        # bar setup
        self.health_bar_rect = pg.Rect(15, 15, 250, 25)

    def show_bar(self, current, max_amount, bg_rect, color):
        pg.draw.rect(self.display_surface, 'white', bg_rect)

        # determine the ratio of the health bar
        ratio = current/max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # display the health bar
        pg.draw.rect(self.display_surface, color, current_rect)

    def show_text(self, current, max_amount):
        self.health_surf = self.font.render(
            f'Health: {int(current)}/{int(max_amount)}', False, 'white')
        self.health_rect = self.health_surf.get_rect(
            topleft=self.health_bar_rect.bottomleft)

        self.display_surface.blit(self.health_surf, self.health_rect)

    def show_exp(self, exp):
        text_surf = self.font.render(f'Exp: {int(exp)}', False, 'white')
        text_rect = text_surf.get_rect(topleft=self.health_rect.bottomleft)

        self.display_surface.blit(text_surf, text_rect)

    def display_waves(self,enemy_amount,wave):
        enemy_surf = self.font.render(f'Enemies Alive: {int(enemy_amount)}', True, 'white')
        wave_surf = self.font.render(f'Wave: {int(wave)}', True, 'white')

        enemy_rect = enemy_surf.get_rect(topleft=(275, 40))
        wave_rect = wave_surf.get_rect(topleft=enemy_rect.bottomleft)

        self.display_surface.blit(enemy_surf, enemy_rect)
        self.display_surface.blit(wave_surf, wave_rect)

    def display_next_wave(self,wave):
        
        next_wave_surf = self.font.render(f'Wave {int(wave)} Complete', True, 'white')
        boss_surf = self.font.render('Boss Cathedral Unlocked', True, 'white')

        next_wave_rect = next_wave_surf.get_rect(topleft=(self.display_surface.get_width()/2 -  next_wave_surf.get_width()/2, self.display_surface.get_height()/2 - 100))
        boss_rect = boss_surf.get_rect(topleft=(self.display_surface.get_width()/2 -  boss_surf.get_width()/2,next_wave_rect.bottom))
        
        self.display_surface.blit(next_wave_surf, next_wave_rect)

        if wave == 5:
            self.display_surface.blit(boss_surf, boss_rect)

    def display(self, player):
        self.show_bar(
            player.health, player.stats['health'], self.health_bar_rect, 'red')

        self.show_text(player.health, player.stats['health'])

        self.show_exp(player.exp)