import pygame
import pytmx

pygame.init()

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 384

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
lvl = pytmx.load_pygame('levels/templates/lvl_2.tmx')
t_width, t_height = lvl.tilewidth, lvl.tileheight

# Loading the bg image from a layer doesn't seem to work...
img = pygame.image.load('levels/bg_512x384.png')
screen.blit(img, (0, 0))


# This just blits the images, instead I should be able to construct
# the sprite groups I think...
plat = lvl.get_layer_by_name('platforms')
for t in plat.tiles():
    screen.blit(t[2], (t[0]*t_width, t[1]*t_height))

obj = lvl.get_layer_by_name('objects')
for t in obj.tiles():
    screen.blit(t[2], (t[0]*t_width, t[1]*t_height))

chars = lvl.get_layer_by_name('characters')
for t in chars.tiles():
    screen.blit(t[2], (t[0]*t_width, t[1]*t_height))

pygame.display.flip()

