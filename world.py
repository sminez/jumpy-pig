import pygame as pg

from config import NEUTRAL_PURPLE, LIGHT0


class Donkey(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load(
            'assets/sprites/donkey.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platform(pg.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pg.Surface([width, height])
        self.image.fill(NEUTRAL_PURPLE)
        self.rect = self.image.get_rect()


class Level:
    level = []

    def __init__(self, player, donkey_xy=(0, 0)):
        self.donkey = Donkey(*donkey_xy)
        self.player = player

        self.platform_list = pg.sprite.Group()
        self.mob_list = pg.sprite.Group(self.donkey)

        self.background = None

        # Go through the array above and add platforms
        for plat in self.level:
            block = Platform(plat[0], plat[1])
            block.rect.x = plat[2]
            block.rect.y = plat[3]
            block.player = self.player
            self.platform_list.add(block)

    def update(self):
        self.platform_list.update()
        self.mob_list.update()

    def draw(self, screen):
        # Draw the background
        screen.fill(LIGHT0)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.mob_list.draw(screen)
