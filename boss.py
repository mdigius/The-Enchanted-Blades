import pygame as pg
import item
from settings import *
from player import Player
import helper
import random
from sounds import Sounds


class Boss(pg.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, damage_player):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics
        self.import_graphics('Demon')
        self.status = 'idle'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.animation_speed = 0.15

        # movement
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-175, -10)
        self.obstacle_sprites = obstacle_sprites
        self.direction = pg.math.Vector2()
        self.pos = pos
        self.item_sprites = pg.sprite.Group()

        # stats
        self.monster_name = 'Demon'
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.total_health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.damage = monster_info['damage']
        self.attack_radius = monster_info['attack_radius']
        self.resistance = monster_info['resistance']
        self.notice_radius = monster_info['notice_radius']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 1800

        # damage display
        self.damage_font = pg.font.Font('imgs/BreatheFireIii-PKLOB.ttf', 20)
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
        self.isIntro = False
        self.boss_health_bar_rect = pg.Rect(
            self.display_surface.get_width()//2-125, 15, 250, 25)
        self.boss_death = False
        self.stop_animation = False
        self.death_animation = False

    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [],
                           'attack': [], 'take_hit': [], 'death': []}
        full_path = f'imgs/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = helper.import_folder(
                full_path + animation)

    def update(self):
        self.move()
        self.animate()
        self.cooldown()
        if not self.vulnerable:
            pg.display.get_surface().blit(self.damage_text, self.damage_text_rect)
        self.boss_health_display()

    def boss_health_display(self):
        pg.draw.rect(self.display_surface, "white", self.boss_health_bar_rect)

        ratio = self.health/self.total_health
        current_width = 250*ratio
        current_rect = pg.Rect(
            self.boss_health_bar_rect)
        current_rect.width = current_width

        pg.draw.rect(self.display_surface, 'red', current_rect)

        self.boss_health_text_surf = self.damage_font.render(
            f'Boss health: {int(self.health)}/{int(self.total_health)}', False, 'white')
        self.boss_health_text_rect = self.boss_health_text_surf.get_rect(
            topleft=(self.boss_health_bar_rect.right + 10, 15))

        self.display_surface.blit(
            self.boss_health_text_surf, self.boss_health_text_rect)

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)

    def animate(self):
        self.animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation):
            if self.status != 'death':
                if self.status == 'attack':
                    self.can_attack = False
                    pg.display.get_surface().get_rect().centerx
                self.frame_index = 0
            else:
                self.stop_animation = True

        # set the image
        if not self.stop_animation:
            self.image = self.animation[int(self.frame_index)]
            if self.direction.x > 0:
                self.image = pg.transform.flip(self.image, True, False)
            elif self.direction.x < 0:
                pass
        elif not self.death_animation:
            if int(self.frame_index) < 22:
                self.image = self.animation[int(self.frame_index)]
                if self.direction.x > 0:
                    self.image = pg.transform.flip(self.image, True, False)
                elif self.direction.x < 0:
                    pass
            self.death_animation = True
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def get_player_distance_direct(self, player):
        boss_vec = pg.math.Vector2(self.rect.center)
        player_vec = pg.math.Vector2(player.rect.center)
        distance = (player_vec - boss_vec).magnitude()

        if distance > 0:
            direction = (player_vec - boss_vec).normalize()
        else:
            direction = pg.math.Vector2()
        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direct(player)[0]
        if self.isIntro:
            self.status = 'idle'
        else:
            if self.health > 0:
                if not self.vulnerable:
                    self.status = 'take_hit'
                else:
                    if distance <= self.attack_radius and self.can_attack:
                        self.status = 'attack'
                    elif distance <= self.notice_radius:
                        self.status = 'move'
            elif self.health <= 0:
                self.status = 'death'
                self.boss_death = True

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
            self.hitbox.y += -self.direction.y * 85
            self.health -= damage
            self.hit_time = pg.time.get_ticks()
            self.vulnerable = False

    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * self.speed
        # self.collision("horizontal")
        self.hitbox.y += self.direction.y * self.speed
        # self.collision("vertical")
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
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving left
                        self.hitbox.top = sprite.hitbox.bottom

    def check_boss_death(self):
        return self.boss_death
