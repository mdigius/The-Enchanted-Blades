import pygame as pg
import enemy
from settings import *
from tile import *
from player import Player
import helper
from pytmx import load_pygame
from npc import Merchant
from shop import Shop
from boss import Boss
from enemy import Enemy
from ui import *
from timer import Timer
import random


class Map:
    def __init__(self, directory, player, startpos, merchant, dungeon, bossRoom):
        self.player = player
        self.active = False
        self.startpos = startpos
        self.npc = pg.sprite.Group()
        self.enemy = pg.sprite.Group()
        self.tmx_data = load_pygame(directory)
        self.door_sprites = pg.sprite.Group()
        self.display_surface = pg.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.visible_sprites.add(self.player)
        self.background_sprites = NoSortCameraGroup()
        self.ground_sprites = NoSortCameraGroup()
        self.obstacles_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.createMap()
        self.game_paused = False
        self.shop = Shop(self.player)
        self.shop_interact = False
        self.set_door_names()
        self.dungeon = False
        self.bossRoom = False
        self.boss = None
        if merchant:
            self.spawn_merchant()
        elif dungeon:
            self.timer = Timer()
            self.dungeon = True
            self.spawn_locations = ((447, 835), (447, 1180), (1208, 1095),
                                    (1603, 492), (1526, 797), (1353, 364), (828, 364))
            self.wave_number = 0
        elif bossRoom:
            self.boss = Boss((259, 160),
                             self.visible_sprites, self.obstacles_sprites, self.damage_player)
            self.bossRoom = True
            self.spawn_boss(self.boss)

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pg.sprite.Group()
        self.attackable_sprites = pg.sprite.Group()

        # user interface
        self.ui = UI()

    def set_active(self, bool):
        self.active = bool
        if self.dungeon:
            self.timer.on_off_timer(bool)

    def spawn_merchant(self):
        self.npc.add(Merchant((150, 45), self.visible_sprites))

    def spawn_enemy(self, name, scale):
        # random number to choose which location on the map the enemy will spawn at
        randl = random.randint(0, 6)
        # random number to offset the enemy in the x direction
        randx = random.randint(-20, 20)
        # random number to offset the enemy in the y direction
        randy = random.randint(-20, 20)
        loc = self.spawn_locations[randl]
        enemyloc = [0, 0]
        enemyloc[0] = loc[0] + randx
        enemyloc[1] = loc[1] + randy
        self.enemy.add(
            Enemy(name, enemyloc, [self.visible_sprites], self.obstacles_sprites, scale, self.damage_player))

    def store_highest_waves(self):
        if self.player.highest_wave < self.wave_number:
            self.player.highest_wave = self.wave_number
            print(self.player.highest_wave)

    def spawn_wave(self):
        if self.wave_number == 0:
            # 5 to start
            for x in range(1):
                self.spawn_enemy('Ooze', 1)

        elif self.wave_number == 1:
            # 10 for wave 2
            for x in range(5):
                self.spawn_enemy('Ooze', 2)
                self.spawn_enemy('RedCap', 2)

        elif self.wave_number == 2:
            # 10 for wave 3
            for x in range(5):
                self.spawn_enemy('RedCap', 2)

            for x in range(5):
                self.spawn_enemy('Eye', 2)

        elif self.wave_number == 3:
            # 20 for wave 4
            for x in range(15):
                self.spawn_enemy('Eye', 2)

            for x in range(5):
                self.spawn_enemy('Ogre', 2)

        elif self.wave_number == 4:
            # 21 for wave 5
            for x in range(10):
                self.spawn_enemy('Eye', 3)
            for x in range(10):
                self.spawn_enemy('Ogre', 3)

        elif self.wave_number == 5:
            for x in range(5):
                self.spawn_enemy('Eye', 4)
            for x in range(15):
                self.spawn_enemy('Ogre', 4)
        else:
            for x in range(20):
                self.spawn_enemy('Ogre', 4)

    def reset_enemy(self):
        for enemy in self.enemy:
            enemy.kill()

    def spawn_boss(self, boss):
        self.enemy.add(boss)

    def set_door_names(self):
        for sprite in self.door_sprites:
            if 980 > sprite.rect.x > 500:
                sprite.set_door_name('Merchant')
            elif sprite.rect.x < 200:
                sprite.set_door_name('MerchantExit')
            elif sprite.rect.x > 1540:
                sprite.set_door_name('Dungeon')
            elif 1120 < sprite.rect.x < 1240:
                sprite.set_door_name('Boss')

    def damage_player(self, amount):
        if self.player.vulnerable:
            self.player.health -= (amount - self.player.armor)
            self.player.vulnerable = False
            self.player.hurt_time = pg.time.get_ticks()
            self.player.sounds.play_audio(self.player.sounds.player_damaged, 0)

    def health_regeneration(self):
        if self.player.health < self.player.stats['health']:
            self.player.health += 1

    def run(self):
        if self.active:
            self.background_sprites.custom_draw(self.player)
            self.ground_sprites.custom_draw(self.player)
            self.visible_sprites.custom_draw(self.player)
            if self.game_paused:
                self.shop.display()
            else:
                self.background_sprites.update()
                self.ground_sprites.update()
                self.visible_sprites.update()
                self.door_sprites.update()
                self.visible_sprites.enemy_update(self.player)
                self.player_attack_logic(self.player)
                self.ui.display(self.player)
                if self.boss != None:
                    self.boss.enemy_update(self.player)
                if self.dungeon:
                    self.timer.display_timer()
                    self.ui.display_waves(len(self.enemy), self.wave_number)
                    if len(self.enemy) == 0 and self.wave_number != 0:
                        self.ui.display_next_wave(self.wave_number)
                elif not self.dungeon and not self.boss:
                    self.health_regeneration()

    def createMap(self):
        for layer in self.tmx_data.layers:
            ground_list = {'Ground', 'Carpet', 'Walkthrough objects'}
            object_list = {'Objects', 'Buildings', 'Walls', 'WallOutline'}
            decor_list = {'WallDecor', 'Decorations', 'Castle Decor'}
            for x, y, surf in layer.tiles():
                pos = (x * 16, y * 16)
                if layer.name == 'Doors':
                    Door(pos, (self.visible_sprites, self.door_sprites), surf)
                if layer.name == 'Star Background':
                    Tile(pos, self.background_sprites, surf)
                elif layer.name in ground_list:
                    Tile(pos, self.ground_sprites, surf)
                elif layer.name in object_list:
                    Tile(pos, (self.visible_sprites, self.obstacles_sprites), surf)
                elif layer.name == 'Border':
                    Tile(pos, (self.visible_sprites, self.obstacles_sprites),
                         pg.image.load('imgs/blank.png'))
                elif layer.name in decor_list:
                    Tile(pos, self.visible_sprites, surf)

    def update_player_info(self, pos=0):
        self.player.hitbox.topleft = self.startpos if pos == 0 else pos
        self.player.set_sprites(self.obstacles_sprites,
                                self.door_sprites, self.enemy)

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def player_attack_logic(self, player):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pg.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(player.damage)


class YSortCameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pg.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(
            sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)


class NoSortCameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pg.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
