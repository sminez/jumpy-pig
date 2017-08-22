import pytmx
import pygame as pg


class Donkey(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.image.load(
            'assets/sprites/donkey.png').convert_alpha()
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
        plat_layer = lvl.get_layer_by_name('platforms')
        obj_layer = lvl.get_layer_by_name('objects')

        # Get start and finish positions
        p_pos = next(pig_layer.tiles())
        d_pos = next(donkey_layer.tiles())

        self.player = player
        player.rect.x = p_pos[0] * self.w
        player.rect.y = p_pos[1] * self.h

        self.donkey = Donkey(
                (d_pos[0] - 0.7) * self.w,
                (d_pos[1] - 0.7) * self.h)

        self.platform_list = pg.sprite.Group()
        self.donkey_list = pg.sprite.Group(self.donkey)

        # Same background image for each level at the moment
        self.background = pg.image.load('levels/bg_512x384.png')

        # Build all of the platforms
        for plat in plat_layer.tiles():
            block = Platform(plat[2])
            block.rect.x = plat[0] * self.w
            block.rect.y = plat[1] * self.h
            # block.player = self.player
            self.platform_list.add(block)

        # Collect the objects and decorations
        self.objects = [o for o in obj_layer.tiles()]

    def update(self):
        self.platform_list.update()
        self.donkey_list.update()

    def draw(self, screen):
        # Draw the background
        screen.blit(self.background, (0, 0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.donkey_list.draw(screen)

        for t in self.objects:
            screen.blit(t[2], (t[0]*self.w, t[1]*self.h))
