import pygame as pg
from config import FADED_PURPLE
from config import SCREEN_HEIGHT, GRAVITY_MOD


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([40, 60])
        self.image.fill(FADED_PURPLE)

        # Make the top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        # Set speed vector
        self.change_x = 0
        self.change_y = 0

        # Current level to interact with
        self.level = None

    def update(self):
        '''Move the player and compute interactions'''
        self.calc_grav()

        # Left/Right
        self.rect.x += self.change_x
        block_hit_list = pg.sprite.spritecollide(
            self, self.level.platform_list, False)

        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # Up/Down
        self.rect.y += self.change_y
        block_hit_list = pg.sprite.spritecollide(
            self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

    def calc_grav(self):
        '''Calculate the effect of gravity'''
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY_MOD

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and \
                self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pg.sprite.spritecollide(
            self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def move_left(self):
        self.change_x = -6

    def move_right(self):
        self.change_x = 6

    def stop(self):
        self.change_x = 0
