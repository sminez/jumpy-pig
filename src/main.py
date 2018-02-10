'''
My daughter loves pigs.
I love games.

Say hello to Jumpy Pig:

         __,---.__        Oink!
      ,-'         `-.__  /
    &/           `._\ _\
    /               ''._
    |   ,             (")
    |__,'`-..--|__|--''
'''
import os
import pygame as pg

from .world import Level
from .player import Player
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, FRAME_RATE, LIGHT0


def get_path(path):
    return os.path.join(os.path.dirname(__file__), path)


def main(level_file='levels.txt', xmas=False, fullsize=True):
    # NOTE: Need to init the audio mixer _before_ the main pygame.init()
    if xmas:
        pg.mixer.pre_init(48000, -16, 2, 2048)
        music_path = get_path('assets/sounds/bruce-comin-to-town.mp3')
    else:
        pg.mixer.pre_init(44100, -16, 2, 2048)
        music_path = get_path('assets/sounds/bg_music1.mp3')

    pg.mixer.init()
    pg.init()

    clock = pg.time.Clock()
    font = pg.font.Font(None, 25)

    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    if fullsize:
        screen = pg.display.set_mode(size, pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode(size)

    pg.display.set_caption("Jumpy Pig! (A Game For Lila)")

    pg.joystick.init()
    # Look for multiple controllers

    count = pg.joystick.get_count()

    if count > 0:
        pad1 = pg.joystick.Joystick(0)
        pad1.init()
        USE_GAMEPAD = True
        pads = [pad1]
        if count == 2:
            pad2 = pg.joystick.Joystick(1)
            pad2.init()
            pads.append(pad2)
    else:
        count = 1
        USE_GAMEPAD = False

    players = [Player(player_ix=ix, is_xmas=xmas) for ix in range(count)]

    # Set up the levels
    with open(get_path(level_file), 'r') as f:
        level_list = [get_path(line.strip()) for line in f]

    current_level_no = 0
    current_level = Level(players, level_list[current_level_no], xmas)

    # Collect all of the sprites
    active_sprite_list = pg.sprite.Group()
    for p in players:
        active_sprite_list.add(p)
        # NOTE: uncomment to display the player hitbox
        # active_sprite_list.add(p, p.hitbox)
        p.level = current_level

    # Start the background music
    pg.mixer.music.load(music_path)
    pg.mixer.music.play(loops=-1)
    pg.mixer.music.set_volume(0.4)

    level_complete_sound = pg.mixer.Sound(
        get_path('assets/sounds/victory-pig.wav'))
    level_complete_sound.set_volume(0.3)

    running = True
    reset = False   # Used to reset to the first level
    frame_no = 0

    # Start the event loop
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if USE_GAMEPAD:
                for ix, pad in enumerate(pads):
                    # Gamepad input using my SNES pads
                    HORIZONTAL = pad.get_axis(0)
                    # VERTICAL = pad.get_axis(1)
                    # X = pad.get_button(0)
                    A = pad.get_button(1)
                    B = pad.get_button(2)
                    # Y = pad.get_button(3)
                    L_SHOULDER = pad.get_button(4)
                    R_SHOULDER = pad.get_button(6)
                    SELECT = pad.get_button(8)
                    START = pad.get_button(9)

                    if HORIZONTAL < 0:
                        players[ix].move_left()
                    if HORIZONTAL > 0:
                        players[ix].move_right()
                    if HORIZONTAL == 0:
                        players[ix].stop()
                    if B == 1 or A == 1:
                        players[ix].jump()
                    if B == 0 and A == 0:
                        players[ix].end_jump()
                    if SELECT == 1 and L_SHOULDER == 1 and R_SHOULDER == 1:
                        running = False
                    if START == 1:
                        reset = True
            else:
                # Keyboard input
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        players[0].move_left()
                    if event.key == pg.K_RIGHT:
                        players[0].move_right()
                    if event.key == pg.K_SPACE:
                        players[0].jump()
                    if event.key == pg.K_q:
                        running = False
                    if event.key == pg.K_r:
                        reset = True

                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT and players[0].change_x < 0:
                        players[0].stop()
                    if event.key == pg.K_RIGHT and players[0].change_x > 0:
                        players[0].stop()

        # Track play time
        seconds = str(frame_no * 10 // FRAME_RATE)
        seconds = 'TIME: ' + (4 - len(seconds)) * '0' + seconds
        frame_no += 1

        # Update the frame
        active_sprite_list.update()
        current_level.update()

        # Keep the player in bounds
        for player in players:
            if player.rect.right > SCREEN_WIDTH:
                player.rect.right = SCREEN_WIDTH

            if player.rect.left < 0:
                player.rect.left = 0

        # NOTE: All drawing code needs to go here!
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        time = font.render(seconds, True, LIGHT0)
        screen.blit(time, (SCREEN_WIDTH-110, 15))

        # Trigger end of level and load the next level
        donkey_hits = [
            pg.sprite.collide_rect(p, current_level.donkey)
            for p in players
        ]
        if any(donkey_hits):
            current_level_no += 1
            if current_level_no == len(level_list):
                pg.mixer.music.stop()
                pg.mixer.music.load(get_path('assets/sounds/victory.mp3'))
                pg.mixer.music.play(loops=-1)
                pg.mixer.music.set_volume(0.4)

                while running:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            running = False

                        if USE_GAMEPAD:
                            for pad in pads:
                                if pad.get_button(8) == 1:
                                    running = False
                                if pad.get_button(9) == 1:
                                    reset = True
                                    running = False
                        else:
                            if event.type == pg.KEYDOWN:
                                if event.key == pg.K_q:
                                    running = False
                                if event.key == pg.K_r:
                                    reset = True
                                    running = False
                if reset:
                    running = True
            else:
                # level_complete_sound.play()
                current_level = Level(players, level_list[current_level_no])
                for player in players:
                    player.level = current_level
                    player.reset()

        # Allow the player to reset to level 1
        if reset:
            reset = False
            current_level_no = 0
            frame_no = 0
            current_level = Level(players, level_list[current_level_no])
            for player in players:
                player.level = current_level
                player.reset()
            pg.mixer.music.stop()
            pg.mixer.music.load(music_path)
            pg.mixer.music.play(loops=-1)
            pg.mixer.music.set_volume(0.4)

        clock.tick(FRAME_RATE)
        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
