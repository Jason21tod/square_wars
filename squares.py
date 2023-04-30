import pygame
from assets import *
from bullets import *
from typing import Iterable



class AbstractSquare(pygame.sprite.Sprite):
    """Classe base dos quadrados do jogo, possui todos os métodos comuns de um quadrado

    Args:
        sprite (Sprite): pygame.sprite
    """
    frame_set = 1
    def __init__(self) -> None:
        super().__init__()
        self.image: pygame.Surface = pygame.Surface((SQUARE_SIZES, SQUARE_SIZES))
        self.color = (0,0,0)
        self.image.fill(self.color)
        self.rect = pygame.draw.rect(self.image, self.color, (0, 0, SQUARE_SIZES, SQUARE_SIZES))

        self.rect.x = 0
        self.rect.y = 0
        self.speed: int = 30

        self.my_bullet = None
        self.bullet_group: pygame.sprite.Group = pygame.sprite.Group
        self.min_distance = MIN_DISTANCE

        self.font = pygame.font.Font(None, 20)
        self.enemies_groups: list[pygame.sprite.Group] = list()
        self.team: str = 'Abstract'
        

    def search_for_enemies(self):
        """Procura por inimigos na lista de inimigos que estejam proximos do raio de alcance dos tiros

        Args:
            enemy_group ( sprite.Group ): Grupo de inimigos a ser analisado.
        """
        for group in self.enemies_groups:
            for square in group.sprites():
                distance = calculate_distance(self, square)
                if distance < self.min_distance:
                    print(f'inimigo detectado: {square.__class__.__name__} [{square.rect.x}, {square.rect.y}]')
                    print(f'Mirando na: [{self.rect.x}, {self.rect.y}]')
                    self.shoot(square)
                    break

    def shoot(self, square: pygame.sprite.Sprite):
        """Cria uma bala e atira de acordo com frame_set do square

        Args:
            square (Square): alvo a ser atingido
        """
        if self.frame_set%30 == 0:
            circle: Bullet = self.my_bullet(self, [square.rect.x,square.rect.y], )
            self.bullet_group.add(circle)
            self.bullet_group.draw(window)
            print(f'disparando...')

    @classmethod
    def update_frame_set(cls):
        if cls.frame_set%400 == 0:
            cls.frame_set = 0
        cls.frame_set += 1

    def update(self):
        print('\n\nRelatorio: ', self.__class__.__name__, 'posição: [', self.rect.x, ', ', self.rect.y, ']')
        if SEE_COORDINATES: render_coordinates_aside(self, self.font, self.color)
        random_move(self)
        self.search_for_enemies()




class _BlueSquare(AbstractSquare):
    def __init__(self) -> None:
        super().__init__()
        self.color = blue
        self.bullet_group = blue_bullet_group
        self.rect.x = randint(0, width//2)
        self.rect.y = randint(0, height//2)
        self.image.fill(self.color)
        self.rect = pygame.draw.rect(self.image, self.color, (0, 0, SQUARE_SIZES, SQUARE_SIZES))
        self.my_bullet = BlueBullet
        self.bullet_group = blue_bullet_group
        self.enemies_groups.append(red_square_group)
        self.team: str = 'azul'


class _RedSquare(AbstractSquare):
    def __init__(self) -> None:
        super().__init__()
        self.color = red
        self.bullet_group = red_bullet_group
        self.rect.x = randint(0, width)
        self.rect.y = randint(0, height)
        self.image.fill(self.color)
        self.rect = pygame.draw.rect(self.image, self.color, (0, 0, SQUARE_SIZES, SQUARE_SIZES))
        self.my_bullet = RedBullet
        self.bullet_group = red_bullet_group
        self.enemies_groups.append(blue_square_group)
        self.team: str = 'vermelho'


red_square_group = pygame.sprite.Group()
blue_square_group = pygame.sprite.Group()


class GroupsHandler:
    """Responsavel por lidar com os grupos de forma coletiva, fazendo update de grupos.
    Atua como um grupo para grupos do pygame

    Raises:
        KeyError: Caso de erro de grupo não encontrado em Groups
    """
    __groups: dict =  {}

    @classmethod
    def register_group(cls, group: pygame.sprite.Group | Iterable, group_name: str | Iterable):
        if type(group) in [dict, list, tuple]:
            if type(group_name) not in [dict, list, tuple]: raise Exception(f'O objeto {group} é um iterável - o argumento {group_name} precisa ser tambem')
            for index, pack in enumerate(group): cls.__groups.update({f'{group_name[index]}': [pack, [] ]})
            print(f'groups: {cls.__groups}')
            return
        elif type(group_name) in [dict, list, tuple]: raise Exception(f'O objeto {group} não é um iterável - o argumento {group_name} não pode ser também')
        cls.__groups.update({f'{group_name}': [group, [] ]})
        print(f'groups: {cls.__groups}')

    @classmethod
    def _verify_group_exists(cls, group_name):
        try:
            groups_list: list = cls.__groups[group_name][1]
            print(groups_list)
        except KeyError:
            raise KeyError(f'O grupo ({group_name}) de sprites espcíficado não pode ser encontrado, veirifique se ele está na lista')
            
    @classmethod
    def register_sprite_to_group(cls, sprite: pygame.sprite.Sprite, group_name: str):
        cls._verify_group_exists(group_name)
        groups_list: list = cls.__groups[group_name][1]
        verify_sprite_errors(sprite)
        if sprite not in groups_list:
            groups_list.append(sprite)
        else: print('Sprite nao adicionada: Ja esta no grupo selecionado')

    @classmethod
    def add_sprites_to_their_groups(cls):
        for group in cls.__groups.items():
            sprite_group: pygame.sprite.Group = group[1][0]
            for sprite in group[1][1]:
                    sprite_group.add(sprite)
    
    @classmethod
    def see_groups(cls):
        for every_group in cls.__groups.items():
            print(every_group[0], ' : ', every_group[1])

    @classmethod
    def update_groups(cls, groups: str | Iterable, ):
        if isinstance(groups,Iterable):
            for name in groups:
                cls.update_single_group(name)
        cls.update_single_group(name)

    @classmethod
    def update_single_group(cls, name):
        cls._verify_group_exists(name)
        group: pygame.sprite.Group = cls.__groups[name][0]
        print(group, 'UPDATED')
        group.update() 
    
    @classmethod
    def draw_groups(cls, surface: pygame.Surface):
        for group in cls.__groups.items():
            sprite_group: pygame.sprite.Group = group[1][0]
            print(sprite_group, 'DRAWED')
            sprite_group.draw(surface)


if __name__ == '__main__':

    print('\nRegistramos o grupo primeiro')
    GroupsHandler.register_group([blue_bullet_group, red_bullet_group], ['grupo balas azul', 'grupo vermelhas'])
    GroupsHandler.see_groups()

    print('\nApós isso, adicionamos um objeto sprite ao grupo...')
    this_sprite = pygame.sprite.Sprite()
    GroupsHandler.register_sprite_to_group(this_sprite, 'grupo vermelhas')

    print('\nN podemos adicionar o mesmo objeto sprite ao grupo...')
    GroupsHandler.register_sprite_to_group(this_sprite, 'grupo vermelhas')
    GroupsHandler.see_groups()

    GroupsHandler.add_sprites_to_their_groups()
    GroupsHandler.see_groups()
