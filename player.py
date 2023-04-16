import pygame as pg
from settings import *
import helper
from sounds import Sounds
from math import sin
from dialogue import Dialogue


# player class
class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.enemy_sprites = None
        self.animations = None
        self.image = pg.image.load(
            'imgs/player/down_idle/WarriorDownIdle1.png')
        self.import_player_assets()

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-35, -20)
        self.attack_hitbox = self.hitbox.inflate(20, 20)
        self.status = 'down_idle'
        self.attacking = False
        self.attack_cooldown = 600
        self.attack_time = 0
        self.frame_index = 0
        self.animation_speed = 0.15
        self.current_room = 0
        # initializes the 2d direction vector and speed value
        self.direction = pg.math.Vector2()
        self.speed = 2
        # takes in the obstacle sprites group from the map class so the player knows
        # where the obstacle sprites are located
        self.obstacle_sprites = None
        self.door_sprites = None
        # stats
        self.stats = {'health': 100, 'damage': 10, 'speed': 5, 'armor': 1}
        self.upgrade_stats = {'health': 100,
                              'damage': 10, 'speed': 1, 'armor': 1}
        self.stats_level = {'health': 1, 'damage': 1, 'speed': 1, 'armor': 1}
        self.max_stats = {'health': 500,
                          'damage': 50, 'speed': 8, 'armor': 20}

        self.upgrade_cost = {'health': 100,
                             'damage': 100, 'speed': 100, 'armor': 100}
        self.exp = 500
        self.health = self.stats['health']
        self.damage = self.stats['damage']
        self.armor = self.stats['armor']

        # sounds
        self.sounds = Sounds()

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        self.highest_wave = 0
        self.bossIntro = False
        self.dialogue = Dialogue()

    def set_sprites(self, obstacle_sprites, door_sprites, enemy_sprites):
        self.obstacle_sprites = obstacle_sprites
        self.door_sprites = door_sprites
        self.enemy_sprites = enemy_sprites

    def import_player_assets(self):
        character_path = 'imgs/player/'
        self.animations = {'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up': [], 'down': [], 'left': [], 'right': [],
                           'up_attack1': [], 'down_attack1': [], 'left_attack1': [], 'right_attack1': []}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = helper.import_folder(full_path)

    def move(self, speed):
        if not self.bossIntro:
            # movement method
            if self.direction.magnitude() != 0:
                # normalizes the vector so that its length is always 1
                # avoids issue where speed is greater when moving diagonally
                self.direction = self.direction.normalize()
            # changes the rect values by the direction vector * speed
            # also calls the collision method to check both vertical and horizontal collisions
            self.hitbox.x += self.direction.x * speed
            self.collision('h')
            self.hitbox.y += self.direction.y * speed
            self.collision('v')
            self.rect.center = self.hitbox.center
            self.attack_hitbox = self.hitbox.inflate(20, 20)

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def get_level_by_index(self, index):
        return list(self.stats_level.values())[index]

    def input(self):
        # gets the key inputs from the pygame module and stores it in a variable
        keys = pg.key.get_pressed()
        # changes the direction of the player based on the key pressed
        if keys[pg.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pg.K_s]:
            self.direction.y = 1
            self.status = 'down'
            # resets direction to 0 if no key is currently being pressed
        else:
            self.direction.y = 0
        if keys[pg.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pg.K_d]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
            # attack inputs
        if keys[pg.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pg.time.get_ticks()

            # play sound when attacking
            self.sounds.play_audio(self.sounds.attack, 0)

    def update(self):
        # update method to call the input method and move the player
        self.input()
        self.cooldown()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])

    def cooldown(self):
        current_time = pg.time.get_ticks()
        if current_time - self.attack_time > self.attack_cooldown:
            self.attacking = False

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack1' in self.status:
                self.status = self.status + '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not '_attack1' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack1')
                else:
                    self.status = self.status + '_attack1'

        else:
            self.status = self.status.replace('_attack1', '')

    def enter_door(self):
        pass

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def collision(self, direction):
        # collision detection method with one argument for vertical and horizontal
        if direction == 'h':
            # checks if there is any collisions with the sprite if it is moving horizontally
            # if so, depending on the direction will move the player to left or right of obstacle
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        # same concept as above but for the vertical collisions
        if direction == 'v':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
        for sprite in self.door_sprites:
            if sprite.hitbox.colliderect(self.hitbox):
                if sprite.door_name == 'Merchant':
                    self.current_room = 1
                elif sprite.door_name == 'MerchantExit':
                    self.current_room = 2
                elif sprite.door_name == 'Dungeon':
                    self.current_room = 3
                elif sprite.door_name == 'Boss':
                    self.current_room = 6
        for sprite in self.enemy_sprites:
            if sprite.hitbox.colliderect(self.attack_hitbox):
                if self.attacking:
                    self.sounds.play_audio(self.sounds.enemy_damaged, 0)
                    sprite.get_damage(self.stats.get('damage'), self)

    def wave_value(self):
        value = sin(pg.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
