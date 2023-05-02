from __future__ import annotations

import sys
import pygame


from random import randint
from pygame import (QUIT,event, display,
                    time, font)

from bullets import red_bullet_group, blue_bullet_group
from squares import AbstractSquare ,_RedSquare, _BlueSquare, GroupsHandler, red_square_group, blue_square_group
from assets import height, width, window, white, red, blue, verify_colisions



GroupsHandler.register_group([red_square_group, blue_square_group], ['vermelho', 'azul'])
GroupsHandler.register_group([red_bullet_group, blue_bullet_group], ['red bullet', 'blue bullet'])


for n in range(0, 7):
    GroupsHandler.create_square_to_group(_RedSquare, [randint(0, int(width//2)), randint(0, int(height//2))], 'vermelho')
    GroupsHandler.create_square_to_group(_BlueSquare, [randint(0, int(width)), randint(0, int(height))], 'azul')

GroupsHandler.add_sprites_to_their_groups()
GroupsHandler.see_groups()


print(display.Info())
clock = time.Clock()


tittle_font = font.Font(None, 50)
text_pos = (height//2, width//2)

while True:
    AbstractSquare.update_frame_set()
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()

    clock.tick(30)
    window.fill(white)
    GroupsHandler.draw_groups(window)

    verify_colisions(red_square_group, blue_bullet_group)
    verify_colisions(blue_square_group, red_bullet_group)

    GroupsHandler.update_groups(['azul', 'vermelho','red bullet', 'blue bullet'])
    

    if len(red_square_group) ==0:
        text_surface = tittle_font.render(f'O time AZUL GANHOU !', True, blue)
        window.blit(text_surface, text_pos)
        print('Vitoria do time Azul')
    if len(blue_square_group) ==0:
        text_surface = tittle_font.render(f'O time VERMELHO GANHOU !', True, red)
        window.blit(text_surface, text_pos)
        print('Vitoria do time vermelho')

    display.flip()