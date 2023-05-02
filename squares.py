import pygame
from assets import *
from bullets import *
from typing import Iterable


SQUARES_SPEED = 30
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
        self.speed: int = SQUARES_SPEED

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
            bullet: Bullet = self.my_bullet(self, [square.rect.x,square.rect.y], )
            self.bullet_group.add(bullet)
            self.bullet_group.draw(window)
            print(f'disparando...')

    @classmethod
    def update_frame_set(cls):
        """Método que faz o update dos sets de frames de maneira global , ou seja: Todas as classes terão
        o mesmo frameset, oque significa que elas estarão no 'mesmo tempo'.
        """
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

    def update(self):
        self.make_clones()
        return super().update()

    def make_clones(self):
        if self.frame_set % 100 ==0:
            red_square_clone = _RedSquareClone()
            red_square_clone.image.fill(pygame.color.Color(0,0,0))
            red_square_clone.rect.x = self.rect.x
            red_square_clone.rect.y = self.rect.y
            self.groups()[0].add(red_square_clone)


class _RedSquareClone(_RedSquare):
    clone_count = 0
    def __init__(self) -> None:
        super().__init__()
        self.speed = int(SQUARES_SPEED + SQUARES_SPEED*0.5)

    def make_clones(self):
        pass

    def update(self):
        self.update_frame_set()
        print('Contador do clone: ', self.clone_count)
        if self.clone_count ==70:
            self.kill()
            self.clone_count = 0
        self.clone_count += 1
        return super().update()

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

    @classmethod
    def create_square_to_group(cls, square_object: AbstractSquare, coordinates: list[int, int], group_name: str):
        """Cria um quadrado com as informações de coordenadas pré-definidas

        Args:
            square_object (AbstractSquare): Objeto do tipo square. 
                - NOTA: O objeto precisa ser um objeto do tipo, não deve ser passada uma instância:
                EXEMPLO:\n\n
                
                    create_square_to_group(_BlueSquare, [randint(0, int(width)), randint(0, int(height))], 'azul')
                

                O objeto passado acima não é uma instância e sim a própria classe

            coordinates (list[int, int]): lista com os dois inteiros onde ele deve ser renderizado
            group_name (str): nome do grupo onde ele será adicionado
        """
        square = square_object()
        square.rect.x = coordinates[0]
        square.rect.y = coordinates[1]
        cls.register_sprite_to_group(square, group_name)


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
