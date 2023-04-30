from pygame.sprite import AbstractGroup
from assets import *
from pygame import sprite, Surface, color, SRCALPHA
import pygame

class Bullet(sprite.Sprite):
    """Classe que representa uma bala comum no jogo, ela pode ser alterada e só possui um
    comportamento no update, movimento retilineo até o local especifico

    Args:
        sprite (Sprite): pygame.sprite.Sprite
    """
    def __init__(self,owner, target_position: list[int]) -> None:
        super().__init__()
        self.image: Surface = Surface((BULLET_SIZE,BULLET_SIZE), SRCALPHA)
        self.color: pygame.color.Color = owner.color
        self.rect = pygame.draw.circle(self.image, self.color, (10, 10), 5)
        
        self.rect.x = owner.rect.x
        self.rect.y = owner.rect.y
        self.font = pygame.font.Font(None, 20)

        self.target_position: list[int] = target_position
        self.coefficient_x = 0
        self.coefficient_y = 0

        self.group: pygame.sprite.Group = pygame.sprite.Group 
        print(f'Invocando circulo na posição[{self.rect.x}, {self.rect.y}]')

    def log_circle_positions(self):
        """Função responsável por mostrar as informações de coordenadas do circulo, todos os logs adicionais
            relacionadas a posição devem ficar aqui.
        """
        print('mirando na posicao: ',self.target_position[0], self.target_position[1])
        print('posicao atual: ', self.rect.x, self.rect.y)
        print('coeficientes: ', self.coefficient_x, self.coefficient_y)

    def verify_do_kill_distance(self):
        """Utiliza regra pitagoras para calcular a distancia do projetil até a posição do alvo
        """
        distance = (self.coefficient_x ** 2 + self.coefficient_y ** 2) ** 0.5
        if distance == 0.0:
            self.kill()
        print('Distancia até o alvo: ', distance)
    
    def move(self):
        """Movimenta a bala em direção a posição do alvo
        """
        x_distance = self.rect.x - self.target_position[0]
        y_distance = self.rect.y - self.target_position[1]
        self.coefficient_x = int(-x_distance*(0.3))
        self.coefficient_y = int(-y_distance*(0.3))
        self.rect.move_ip(self.coefficient_x, self.coefficient_y)

    def update(self) -> None:
        if SEE_COORDINATES: render_coordinates_aside(self, self.font, self.color)
        self.log_circle_positions()
        self.move()
        self.verify_do_kill_distance()


red_bullet_group = sprite.Group()
blue_bullet_group = sprite.Group()


class BlueBullet(Bullet):
    def __init__(self, owner, target_position: list[int]) -> None:
        super().__init__(owner, target_position)
        self.group = blue_bullet_group

class RedBullet(Bullet):
    def __init__(self, owner, target_position: list[int]) -> None:
        super().__init__(owner, target_position)
        self.group = red_bullet_group


