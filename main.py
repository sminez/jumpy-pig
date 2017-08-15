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

from player import Player
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from levels import Level_01, Level_02, Level_XX


def main():
    pg.init()
    clock = pg.time.Clock()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pg.display.set_mode(size)
    pg.display.set_caption("Jumpy Pig! (A Game For Lila)")

    player = Player()

    # Set up the levels
    level_list = [Level_01, Level_02, Level_XX]
    level_list = [l(player) for l in level_list]
    current_level_no = 2
    current_level = level_list[current_level_no]

    # Collect all of the sprites
    active_sprite_list = pg.sprite.Group()
    active_sprite_list.add(player)
    player.level = current_level

    running = True

    # Start the event loop
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    player.move_left()
                if event.key == pg.K_RIGHT:
                    player.move_right()
                if event.key == pg.K_SPACE:
                    player.jump()

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pg.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update the frame
        active_sprite_list.update()
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0

        # NOTE: All drawing code needs to go here!
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # These should always be the last two lines in the main loop
        clock.tick(60)
        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
