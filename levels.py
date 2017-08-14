from world import Level, Platform


class Level_01(Level):
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
