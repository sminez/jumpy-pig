from world import Level, Platform
from config import SCREEN_HEIGHT


class Level_01(Level):
    '''Move to the right'''
    def __init__(self, player):
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = []

        # Go through the array above and add platforms
        for plat in level:
            block = Platform(plat[0], plat[1])
            block.rect.x = plat[2]
            block.rect.y = plat[3]
            block.player = self.player
            self.platform_list.add(block)

        player.rect.x = 0
        player.rect.y = SCREEN_HEIGHT - player.rect.height


class Level_02(Level):
    '''Jump up onto a step'''
    def __init__(self, player):
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [
            (600, 50, 200, 550),
        ]

        # Go through the array above and add platforms
        for plat in level:
            block = Platform(plat[0], plat[1])
            block.rect.x = plat[2]
            block.rect.y = plat[3]
            block.player = self.player
            self.platform_list.add(block)

        player.rect.x = 0
        player.rect.y = SCREEN_HEIGHT - player.rect.height


class Level_XX(Level):
    '''Actual platforming!'''
    def __init__(self, player):
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [
            (210, 40, 500, 500),
            (200, 40, 200, 400),
            (190, 40, 600, 300),
            (70, 40, 100, 250),
            (140, 40, 350, 150),
            (90, 40, 680, 200),
        ]

        # Go through the array above and add platforms
        for plat in level:
            block = Platform(plat[0], plat[1])
            block.rect.x = plat[2]
            block.rect.y = plat[3]
            block.player = self.player
            self.platform_list.add(block)

        player.rect.x = 340
        player.rect.y = SCREEN_HEIGHT - player.rect.height


