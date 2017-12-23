import os
import pytmx
import pygame as pg


def get_path(path):
    return os.path.join(os.path.dirname(__file__), path)


class Donkey(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load(
            get_path('assets/sprites/donkey.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platform(pg.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()


class Level:
    level = []

    def __init__(self, player, map_path):
        '''Construct a new level from a .tmx file'''
        # Load and parse the level file
        lvl = pytmx.load_pygame(map_path)
        self.w, self.h = lvl.tilewidth, lvl.tileheight

        # Fetch each of the layers
        pig_layer = lvl.get_layer_by_name('pig')
        donkey_layer = lvl.get_layer_by_name('donkey')
        mob_layer = lvl.get_layer_by_name('mobs')
        plat_layer = lvl.get_layer_by_name('platforms')
        obj_layer = lvl.get_layer_by_name('objects')
        col_layer = lvl.get_layer_by_name('collectables')
        # bg_layer = lvl.get_layer_by_name('bg')

        # Get start and finish positions
        p_pos = next(pig_layer.tiles())
        d_pos = next(donkey_layer.tiles())

        self.player = player
        player.rect.x = p_pos[0] * self.w
        player.rect.y = p_pos[1] * self.h

        self.donkey = Donkey(
            # The offset for the donkey sprite is wrong for some reason...!
            (d_pos[0] - 0.7) * self.w,
            (d_pos[1] - 0.7) * self.h)

        self.platform_list = pg.sprite.Group()
        self.donkey_list = pg.sprite.Group(self.donkey)
        # self.mob_list = pg.sprite.Group()

        # Same background image for each level at the moment
        self.background = pg.image.load(
            get_path('levels/tmx-files/xmas/bg_512x384.png'))
            # get_path('levels/bg_512x384.png'))

        # Build all of the platforms
        for plat in plat_layer.tiles():
            block = Platform(plat[2])
            block.rect.x = plat[0] * self.w
            block.rect.y = plat[1] * self.h
            self.platform_list.add(block)

        # Collect the mobs, objects and collectables
        self.mobs = [o for o in mob_layer.tiles()]
        self.objects = [o for o in obj_layer.tiles()]
        self.collectables = [o for o in col_layer.tiles()]

        # Draw all the staic sprite lists that we have to the background
        self.platform_list.draw(self.background)

        # Blit objects (decoration only)
        for t in self.objects:
            self.background.blit(t[2], (t[0]*self.w, t[1]*self.h))

        # Blit collectables
        for t in self.collectables:
            self.background.blit(t[2], (t[0]*self.w, t[1]*self.h))

        self.donkey_list.draw(self.background)

    def update(self):
        # NOTE: Once things move, this will need to be modified
        #       to update sprite positions etc
        pass

    def draw(self, screen):
        '''Draw the current level'''
        screen.blit(self.background, (0, 0))
