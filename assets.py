import pygame

from random import randint
from configs import *


def verify_colisions(sprite_group_a: pygame.sprite.Group, sprite_group_b:pygame.sprite.Group):
    """Verifica a colisão dos grupos e mata o grupo concorrente em caso de colisão:

    Args:
        sprite_group_a (pygame.sprite.Group): Grupo que colide. Este grupo deleta o grupo B
        sprite_group_b (pygame.sprite.Group): Grupo a ser colidido. Este grupo é deletado pelo grupo A.
    """
    colision_dict: dict[pygame.sprite.Sprite] = pygame.sprite.groupcollide( sprite_group_a, sprite_group_b, False, False)
    if len(colision_dict) != 0:
        print(f'Colisões detectadas {sprite_group_a} >>> {sprite_group_b}')
        for sprite in colision_dict:
            sprite.kill()

def verify_sprite_errors(sprite):
    """Verifica se a Sprite está de acordo com os padrões do sistema: Ela precisa possuir os atributos rect e speed

    Args:
        sprite (pygame.sprite.Sprite): Objeto sprite em questão
    """
    try:
        sprite.speed
        sprite.rect
        int(sprite.speed)
    except Exception:
        Exception('\n\nO valor inserido não é uma sprite ou não possui o atributo speed do tipo inteiro\n\n')

def calculate_distance(sprite: pygame.sprite.Sprite, target: pygame.sprite.Sprite):
    """Calcula a distancia entre 2 sprite.

    Args:
        sprite (sprite.Sprite): Sprite usado como ponto A
        target (sprite.Sprite): Sprite usado como ponto B

    Returns:
        int: Distancia entre os dois pontos
    """
    verify_sprite_errors(sprite)
    dx = sprite.rect.x - target.rect.x
    dy = sprite.rect.y - target.rect.y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    print(f'distância x: {dx} | distância y: {dy}')
    print({distance})
    return distance

def render_coordinates_aside(sprite_objct: pygame.sprite.Sprite, font:pygame.font.Font, color: pygame.color.Color):
    """Gera texto com as coordenadas do objeto em x, y ao lado dele

    Args:
        sprite_objct (sprite.Sprite): Um objeto sprite com um uma rect 
        font (font.Font): um objeto do tipo fonte para especificar qual fonte será renderizada
        color (color.Color): um objeto do tipo color do pygame

    Raises:
        Exception: Caso o objeto fornecido não seja 
    """
    try:
        text_surface = font.render(f'x:{sprite_objct.rect.x} y:{sprite_objct.rect.y}', True, color)
    except:
        raise Exception('\n\nO objeto fornecido não é do tipo "pygame.font.Font"\n\n')
    text_pos = (sprite_objct.rect.x + sprite_objct.rect.size[0] + 10, sprite_objct.rect.centery - text_surface.get_height()//2)
    window.blit(text_surface, text_pos) 

def random_move(sprite):
    """Movimenta a sprite de forma aleatoria
    Args:
        sprite (sprite.Sprite): Sprite a ser movimentada
    """
    verify_sprite_errors(sprite)
    random_number = randint(0,10)
    move_random_x(sprite, random_number)
    move_random_y(sprite, random_number)


def move_random_x(sprite, random_coin):
    """Movimenta a sprite de acordo com o numero fornecido: 0 para direita, 1 para esquerda

    Args:
        sprite (sprite.Sprite): Sprite a ser movida
        random_coin (int): numero especifico: 0 - 1
    """
    if random_coin == 0:  
        if sprite.rect.x < width - sprite.rect.size[0]: #se for muito para a direita da tela
            sprite.rect.move_ip(sprite.speed, 0)
            return
        sprite.rect.x -= sprite.speed
    if random_coin == 1:
        if sprite.rect.x > 0: #se for muito para a esquerda da tela
            sprite.rect.move_ip(-sprite.speed, 0)
            return
        sprite.rect.x += sprite.speed

def move_random_y(sprite , random_coin):
    """Movimenta a sprite de acordo com o numero fornecido: 2 para baixo, 3 para cima

    Args:
        sprite (sprite.Sprite): Sprite a ser movida
        random_coin (int): numero especifico: 2 - 3
    """
    if random_coin == 2:
        if sprite.rect.y < height - sprite.rect.size[0]: #se for muito para baixo
            sprite.rect.move_ip(0, sprite.speed)
            return
        sprite.rect.y -= sprite.speed
    if random_coin == 3:
        if sprite.rect.y > 0: #se for muito para cima
            sprite.rect.move_ip(0, -sprite.speed)
            return
        sprite.rect.y += sprite.speed
