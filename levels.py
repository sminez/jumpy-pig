from world import Level
from config import SCREEN_HEIGHT, SCREEN_WIDTH


class Level_01(Level):
    '''Move to the right'''
    def __init__(self, player):
        # Array with width, height, x, and y of platform
        self.level = []
        Level.__init__(self, player, (SCREEN_WIDTH - 10, SCREEN_HEIGHT))

        player.rect.x = 0
        player.rect.y = SCREEN_HEIGHT - player.rect.height


class Level_02(Level):
    '''Jump up onto a step'''
    def __init__(self, player):
        # Array with width, height, x, and y of platform
        self.level = [
            (600, 50, 200, 550),
        ]
        Level.__init__(self, player, (SCREEN_WIDTH - 10, SCREEN_HEIGHT))

        player.rect.x = 0
        player.rect.y = SCREEN_HEIGHT - player.rect.height


class Level_XX(Level):
    '''Actual platforming!'''
    def __init__(self, player):
        # Array with width, height, x, and y of platform
        self.level = [
            (210, 40, 500, 500),
            (200, 40, 200, 400),
            (190, 40, 600, 300),
            (70, 40, 100, 250),
            (140, 40, 350, 150),
            (90, 40, 680, 200),
        ]
        Level.__init__(self, player, (100, 170))

        player.rect.x = 340
        player.rect.y = SCREEN_HEIGHT - player.rect.height
