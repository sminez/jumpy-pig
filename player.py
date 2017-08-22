import pygame as pg
# from config import BRIGHT_AQUA
from config import SCREEN_HEIGHT, GRAVITY_MOD, JUMP_SPEED, HITBOX_RATIO, \
        WALK_SPEED, WALK_ANIM_SPEED


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Pig sprites: left and right
        self.image_right = [
            # pg.image.load(
            #     'assets/sprites/alpha-pig-right.png').convert_alpha(),
            # pg.image.load(
            #     'assets/sprites/alpha-pig-right-up.png').convert_alpha()
            pg.image.load(
                'assets/sprites/jumpy/right.png').convert_alpha(),
            pg.image.load(
                'assets/sprites/jumpy/right2.png').convert_alpha(),
        ]
        self.image_left = [
            # pg.image.load(
            #     'assets/sprites/alpha-pig-left.png').convert_alpha(),
            # pg.image.load(
            #     'assets/sprites/alpha-pig-left-up.png').convert_alpha()
            pg.image.load(
                'assets/sprites/jumpy/left.png').convert_alpha(),
            pg.image.load(
                'assets/sprites/jumpy/left2.png').convert_alpha(),
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
        # self.jump_sound = pg.mixer.Sound('assets/sounds/smw_jump.wav')
        self.jump_sound = pg.mixer.Sound('assets/sounds/pig-jump.wav')
        self.jump_sound.set_volume(0.3)

        # Set speed vector
        self.change_x = 0
        self.change_y = 0

        # Current level to interact with
        self.level = None

    def update(self):
        '''Move the player and compute interactions'''
        self.hitbox.rect.midbottom = self.rect.midbottom

        # TODO :: acceleration/momentum
        self.calc_grav()

        # Left/Right movement
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
        # NOTE: We need to check that there is a platform below for us to
        #       jump from. (1px seems to bug out on if the platform is moving
        #       down when we jump)
        self.hitbox.rect.y += 2
        platform_hit_list = pg.sprite.spritecollide(
            self.hitbox, self.level.platform_list, False)
        # Reset position after the collision check
        self.hitbox.rect.y -= 2

        # If it is ok to jump, jump!
        if len(platform_hit_list) > 0 or \
                self.hitbox.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -1 * JUMP_SPEED
            # Play the jump sound
            self.jump_sound.play()

    def move_left(self):
        '''Move left and set the pig to face left'''
        self.change_x = -WALK_SPEED

    def move_right(self):
        '''Move right and send the pig to face right'''
        self.change_x = WALK_SPEED

    def stop(self):
        self.change_x = 0
