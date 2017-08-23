'''
Main file for the game.

Adapted from the tutorial found here:
    http://programarcadegames.com/index.php?chapter=example_code_platformer
    http://programarcadegames.com/index.php?chapter=controllers_and_graphics&lang=en

https://retropie.org.uk/
http://lifehacker.com/how-to-turn-your-raspberry-pi-into-a-retro-game-console-498561192

TODO:
    easy way to make levels
    add Claude to the level as a finish post
'''
import pygame as pg

from world import Level
from player import Player
from config import SCREEN_WIDTH, SCREEN_HEIGHT
# from levels import Level_01, Level_02, Level_XX


def main():
    # NOTE: Need to init the audio mixer _before_ the main pygame.init()
    pg.mixer.pre_init(44100, -16, 2, 2048)
    pg.mixer.init()
    pg.init()

    clock = pg.time.Clock()

    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    # screen = pg.display.set_mode(size)
    screen = pg.display.set_mode(size, pg.FULLSCREEN)
    pg.display.set_caption("Jumpy Pig! (A Game For Lila)")

    pg.joystick.init()
    if pg.joystick.get_count() > 0:
        pad = pg.joystick.Joystick(0)
        pad.init()
        USE_GAMEPAD = True
    else:
        USE_GAMEPAD = False

    player = Player()

    # Set up the levels
    level_list = [
        'levels/templates/lvl_1.tmx',
        'levels/templates/lvl_2.tmx',
        'levels/templates/lvl_3.tmx',
        'levels/templates/lvl_4.tmx',
        'levels/templates/lvl_5.tmx',
        'levels/templates/lvl_6.tmx',
        'levels/templates/lvl_10.tmx'
    ]
    current_level_no = 0
    current_level = Level(player, level_list[current_level_no])

    # Collect all of the sprites
    active_sprite_list = pg.sprite.Group()
    active_sprite_list.add(player)
    # NOTE: uncomment to display the player hitbox
    # active_sprite_list.add(player, player.hitbox)
    player.level = current_level

    running = True
    reset = False   # Used to reset to the first level

    # Start the background music
    pg.mixer.music.load('assets/sounds/bg_music1.mp3')
    pg.mixer.music.play(loops=-1)
    pg.mixer.music.set_volume(0.4)

    # Start the event loop
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # Keyboard input
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    player.move_left()
                if event.key == pg.K_RIGHT:
                    player.move_right()
                if event.key == pg.K_SPACE:
                    player.jump()
                if event.key == pg.K_q:
                    running = False

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pg.K_RIGHT and player.change_x > 0:
                    player.stop()

            if USE_GAMEPAD:
                # Gamepad input using my SNES pads
                HORIZONTAL = pad.get_axis(0)
                # VERTICAL = pad.get_axis(1)
                # X = pad.get_button(0)
                # A = pad.get_button(1)
                B = pad.get_button(2)
                Y = pad.get_button(3)
                # L_SHOULDER = pad.get_button(4)
                # R_SHOULDER = pad.get_button(6)
                SELECT = pad.get_button(8)
                START = pad.get_button(9)

                if HORIZONTAL < 0:
                    player.move_left()
                if HORIZONTAL > 0:
                    player.move_right()
                if HORIZONTAL == 0:
                    player.stop()
                if B == 1 or Y == 1:
                    player.jump()
                if SELECT == 1:
                    running = False
                if START == 1:
                    reset = True

        # Update the frame
        active_sprite_list.update()
        current_level.update()

        # Keep the player in bounds
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        if player.rect.left < 0:
            player.rect.left = 0

        # NOTE: All drawing code needs to go here!
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        if pg.sprite.collide_rect(player, current_level.donkey):
            current_level_no += 1
            if current_level_no == len(level_list):
                current_level_no = 0
            current_level = Level(player, level_list[current_level_no])
            player.level = current_level
            player.image = player.image_right[0]

        if reset:
            reset = False
            current_level_no = 0
            current_level = Level(player, level_list[current_level_no])
            player.level = current_level
            player.image = player.image_right[0]

        # These should always be the last two lines in the main loop
        clock.tick(60)
        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
