import random

import pygame as pg
import item
from settings import *
from player import Player
import helper
from math import sin

from sounds import Sounds


class Enemy(pg.sprite.Sprite):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, scale, damage_player):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.scale = scale
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.animation_speed = 0.15

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites
        self.direction = pg.math.Vector2()
        self.pos = pos
        self.item_sprites = pg.sprite.Group()

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.damage = monster_info['damage']
        self.attack_radius = monster_info['attack_radius']
        self.resistance = monster_info['resistance']
        self.notice_radius = monster_info['notice_radius']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_font = pg.font.Font('imgs/BreatheFireIii-PKLOB.ttf', 18)
        self.damage_text = None
        self.damage_text_rect = None
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # invincibility timer
        self.vulnerable = True
        self.invincible_duration = 300
        self.hit_time = 0

        self.damage_player = damage_player

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []}
        full_path = f'imgs/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = helper.import_folder(
                full_path + animation)

    def add_xp(self, player):
        player.exp += self.exp

    def update(self):
        # self.hit_reaction()
        self.move()
        self.animate()
        self.cooldown()
        if not self.vulnerable:
            pg.display.get_surface().blit(self.damage_text, self.damage_text_rect)

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.checkDeath(player)

    def animate(self):
        self.animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation):
            if self.status == 'attack':
                self.can_attack = False
                pg.display.get_surface().get_rect().centerx
            self.frame_index = 0

        # set the image
        self.image = pg.transform.scale(
            self.animation[int(self.frame_index)], (self.scale*16, self.scale*16))
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_player_distance_direct(self, player):
        monster_vec = pg.math.Vector2(self.rect.center)
        player_vec = pg.math.Vector2(player.rect.center)
        distance = (player_vec - monster_vec).magnitude()

        if distance > 0:
            direction = (player_vec - monster_vec).normalize()
        else:
            direction = pg.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direct(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pg.time.get_ticks()
            self.damage_player(self.damage)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direct(player)[1]
        else:
            self.direction = pg.math.Vector2()

    def cooldown(self):
        current_time = pg.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincible_duration:
                self.vulnerable = True

    def get_damage(self, damage, player):
        if self.vulnerable:
            text = '-' + str(damage)
            self.damage_text = self.damage_font.render(
                text, False, (255, 0, 0))
            self.offset = pg.math.Vector2()
            self.offset.x = player.rect.centerx - \
                self.half_width + random.randint(5, 60)
            self.offset.y = player.rect.centery - \
                self.half_height + random.randint(5, 60)
            self.damage_text_rect = self.damage_text.get_rect()
            self.damage_text_rect.center = self.hitbox.center - self.offset
            self.hitbox.x += -self.direction.x*95
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.x += self.direction.x
                    if self.direction.x < 0:
                        self.hitbox.x -= self.direction.x
            self.hitbox.y += -self.direction.y * 85
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.y += self.direction.y
                    if self.direction.y < 0:
                        self.hitbox.y -= self.direction.y
            self.health -= damage
            self.hit_time = pg.time.get_ticks()
            self.vulnerable = False

    def checkDeath(self, player):
        if self.health <= 0:
            self.add_xp(player)
            if player.health < player.stats['health']:
                player.health += 1
            self.kill()

    def dropItem(self):
        self.drop = item(self.item_sprites, 1, 'Enemy drop',
                         self.pos[0], self.pos[1])

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving left
                        self.hitbox.top = sprite.hitbox.bottom

    def wave_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
