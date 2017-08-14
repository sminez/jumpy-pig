import pygame as pg

from config import FADED_BLUE, NEUTRAL_BLUE


class Platform(pg.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pg.Surface([width, height])
        self.image.fill(FADED_BLUE)
        self.rect = self.image.get_rect()


class Level:
    def __init__(self, player):
        self.platform_list = pg.sprite.Group()
        self.enemy_list = pg.sprite.Group()
        self.player = player
        self.background = None

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        # Draw the background
        screen.fill(NEUTRAL_BLUE)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
