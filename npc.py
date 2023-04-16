import pygame as pg
from settings import *
import helper


class Merchant(pg.sprite.Sprite):
    def __init__(self, pos, groups):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'merchant'

        # graphics
        self.import_npc_assets()
        self.status = 'idle'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
        self.animation_speed = 0.15

    def update(self):
        self.animate()

    def import_npc_assets(self):
        self.animations = {'idle': []}
        full_path = 'imgs/merchant/'
        for animation in self.animations.keys():
            self.animations[animation] = helper.import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def show_shop_items(self):
        pass

    def get_player_distance_direct(self, player):
        merchant_vec = pg.math.Vector2(self.rect.center)
        player_vec = pg.math.Vector2(player.rect.center)
        distance = (player_vec - merchant_vec).magnitude()

        return (distance)

    def get_status(self, player):
        distance = self.get_player_distance_direct(player)

        if distance < 5:
            self.status = 'shop'
        else:
            self.status = 'idle'

    def merchant_status(self):
        return self.status
