import pygame as pg
from config import SCREEN_HEIGHT, GRAVITY_MOD, JUMP_SPEED


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Pig sprites: left and right
        self.image_right = pg.image.load(
            'assets/alpha-pig-right.png').convert_alpha()
        self.image_left = pg.image.load(
            'assets/alpha-pig-left.png').convert_alpha()
        self.image = self.image_right

        # Sounds
        # self.jump_sound = pg.mixer.Sound('assets/smw_jump.wav')
        self.jump_sound = pg.mixer.Sound('assets/pig-jump.wav')
        self.jump_sound.set_volume(0.3)

        # Make the top-left corner the passed-in location.
        self.rect = self.image.get_rect()

        # Set speed vector
        self.change_x = 0
        self.change_y = 0

        # Current level to interact with
        self.level = None

    def update(self):
        '''Move the player and compute interactions'''
        # TODO :: acceleration/momentum
        self.calc_grav()

        # Left/Right movement
        self.rect.x += self.change_x
        block_hit_list = pg.sprite.spritecollide(
            self, self.level.platform_list, False)

        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # Up/Down movement
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
        '''Calculate the effect of gravity on the pig'''
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY_MOD

        # See if we are on the ground and correct
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and \
                self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        # Make the jump sound
        self.jump_sound.play()

        # NOTE: We need to check that there is a platform below for us to
        #       jump from. (1px seems to bug out on if the platform is moving
        #       down when we jump)
        self.rect.y += 2
        platform_hit_list = pg.sprite.spritecollide(
            self, self.level.platform_list, False)
        # Reset position after the collision check
        self.rect.y -= 2

        # If it is ok to jump, jump!
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -1 * JUMP_SPEED

    def move_left(self):
        '''Move left and set the pig to face left'''
        self.change_x = -6
        self.image = self.image_left

    def move_right(self):
        '''Move right and send the pig to face right'''
        self.change_x = 6
        self.image = self.image_right

    def stop(self):
        self.change_x = 0
