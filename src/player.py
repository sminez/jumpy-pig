import os
import pygame as pg
from .config import SCREEN_HEIGHT, GRAVITY_MOD, JUMP_SPEED, HITBOX_RATIO, \
        WALK_SPEED, WALK_ANIM_SPEED, WALK_ACCELERATION, WALK_SLOWDOWN, \
        WALK_STOP_THRESHOLD, WALK_SLOWDOWN_INITIAL


def get_path(path):
    return os.path.join(os.path.dirname(__file__), path)


class Player(pg.sprite.Sprite):
    def __init__(self, player_ix=0, is_xmas=False):
        super().__init__()

        XMAS = 'xmas-' if is_xmas else ''
        self.player_ix = player_ix

        suffix = '-2' if player_ix == 1 else ''

        # Pig sprites: left and right
        self.image_right = [
            pg.image.load(
                get_path('assets/sprites/jumpy/{}right{}.png'.format(XMAS, suffix))
            ).convert_alpha(),
            pg.image.load(
                get_path('assets/sprites/jumpy/{}right2{}.png'.format(XMAS, suffix))
            ).convert_alpha(),
        ]
        self.image_left = [
            pg.image.load(
                get_path('assets/sprites/jumpy/{}left{}.png'.format(XMAS, suffix))
            ).convert_alpha(),
            pg.image.load(
                get_path('assets/sprites/jumpy/{}left2{}.png'.format(XMAS, suffix))
            ).convert_alpha(),
        ]

        self.image = self.image_right[0]
        self.rect = self.image.get_rect()

        # Create a smaller hitbox to work with
        self.hitbox = pg.sprite.Sprite()
        # self.hitbox.image = pg.Surface(
        #     (self.rect.width * HITBOX_RATIO, self.rect.height))
        # self.hitbox.image.fill(BRIGHT_AQUA)

        self.hitbox.rect = pg.rect.Rect(
            (0, 0),
            (self.rect.width * HITBOX_RATIO, self.rect.height))
        # Position the hitbox
        self.hitbox.midbottom = self.rect.midbottom

        # Sounds
        self.jump_sound = pg.mixer.Sound(
            get_path('assets/sounds/pig-jump.wav'))
        self.jump_sound.set_volume(0.3)

        # Set speed vectors
        self.change_x = 0
        self.change_y = 0
        self.stopping = False
        self.jumping = False

        # Current level to interact with
        self.level = None

    def update(self):
        '''Move the player and compute interactions'''
        self.hitbox.rect.midbottom = self.rect.midbottom

        self.calc_grav()

        # Left/Right movement
        if self.stopping:
            self.change_x -= (self.change_x / WALK_SLOWDOWN)
            if -WALK_STOP_THRESHOLD < self.change_x < WALK_STOP_THRESHOLD:
                self.change_x = 0
                self.stopping = False
        elif -WALK_SPEED < self.change_x < 0:
            self.change_x -= WALK_ACCELERATION
            if self.change_x < -WALK_SPEED:
                self.change_x = -WALK_SPEED
        elif WALK_SPEED > self.change_x > 0:
            self.change_x += WALK_ACCELERATION
            if self.change_x > WALK_SPEED:
                self.change_x = WALK_SPEED

        self.rect.x += self.change_x
        self.hitbox.rect.x += self.change_x

        # Animate the movement
        if self.change_x < 0:
            frame = (self.rect.x // WALK_ANIM_SPEED) % len(self.image_left)
            self.image = self.image_left[frame]
        elif self.change_x > 0:
            frame = (self.rect.x // WALK_ANIM_SPEED) % len(self.image_right)
            self.image = self.image_right[frame]

        block_hit_list = pg.sprite.spritecollide(
            self.hitbox, self.level.platform_list, False)

        for block in block_hit_list:
            if self.change_x > 0:
                self.hitbox.rect.right = block.rect.left
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.hitbox.rect.left = block.rect.right
                self.rect.left = block.rect.right

        # Up/Down movement
        self.rect.y += self.change_y
        self.hitbox.rect.y += self.change_y

        block_hit_list = pg.sprite.spritecollide(
            self.hitbox, self.level.platform_list, False)

        for block in block_hit_list:
            if self.change_y > 0:
                self.hitbox.rect.bottom = block.rect.top
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.hitbox.rect.top = block.rect.bottom
                self.rect.top = block.rect.bottom
            self.change_y = 0

    def calc_grav(self):
        '''Calculate the effect of gravity on the pig'''
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += GRAVITY_MOD

        # See if we are on the ground and correct
        if self.hitbox.rect.y >= SCREEN_HEIGHT - self.hitbox.rect.height and \
                self.change_y >= 0:
            self.change_y = 0
            self.hitbox.rect.y = SCREEN_HEIGHT - self.hitbox.rect.height
            self.rect.y = SCREEN_HEIGHT - self.hitbox.rect.height

    def jump(self):
        '''
        We need to check that there is a platform below for us to jump from.
        '''
        self.jumping = True
        self.hitbox.rect.y += 2
        platform_hit_list = pg.sprite.spritecollide(
            self.hitbox, self.level.platform_list, False)
        # Reset position after the collision check
        self.hitbox.rect.y -= 2

        # If it is ok to jump, jump!
        if len(platform_hit_list) > 0 or \
                self.hitbox.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -1 * JUMP_SPEED
            self.jump_sound.play()

    def end_jump(self):
        '''Cut off the jump'''
        self.jumping = False

    def move_left(self):
        '''Move left and set the pig to face left'''
        self.stopping = False
        if self.change_x < 0:
            # Don't reset speed if we are already moving
            return

        self.change_x = -WALK_ACCELERATION

    def move_right(self):
        '''Move right and send the pig to face right'''
        self.stopping = False
        if self.change_x > 0:
            # Don't reset speed if we are already moving
            return

        self.change_x = WALK_ACCELERATION

    def stop(self):
        '''Start slowing down the player'''
        self.change_x *= WALK_SLOWDOWN_INITIAL
        self.stopping = True

    def reset(self):
        '''Called on reset and level load to initilise position'''
        self.image = self.image_right[0]
        if self.change_x < 0:
            self.change_x = 0
        self.change_y = 0
