# импортируем
import os
import sys
import pygame

# файл с лабиринтом
flnam = "lab.txt"
screen = pygame.display.set_mode((550, 500))
# размер плиток
tile_width = tile_height = 50
hp = 100

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


# камера
def r(obj):
    obj.rect.x -= (player.pos[0] - 10) * 50 + 250
    obj.rect.y -= (player.pos[1] - 10) * 50 + 300


# вывод текста
def drawtext(surf, text, size, x, y):
    font = pygame.font.Font("Arial.ttf", size)
    text_surface = font.render(text, True, pygame.Color('WHITE'))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# проверка на наличие файла
def load_image(name):
    fn = os.path.join('data1', name)
    if not os.path.isfile(fn):
        print(f"Файл '{fn}' не найден")
        sys.exit()
    image = pygame.image.load(fn)
    return image


# Виды плиток
images = {'wall': pygame.transform.scale(load_image('cobblestone.png'), (50, 50)),
          'grass': pygame.transform.scale(load_image('grass.jpg'), (50, 50)),
          'wall1': pygame.transform.scale(load_image('brick.png'), (50, 50)),
          'cross': pygame.transform.scale(load_image('cross.jpg'), (50, 50)),
          'trap': pygame.transform.scale(load_image('trap.jpg'), (50, 50)),
          }
player_image = pygame.transform.scale(load_image('knight.png'), (50, 50))


class Camera:
    def __init__(self):
        self.px = 0
        self.py = 0

    # смещение камеры
    def apply(self, obj):
        obj.rect.x += self.px
        obj.rect.y += self.py

    # перемещение персонажа
    def ud(self, n):
        if n == '4':
            self.px = 50
            self.py = 0
        elif n == '3':
            self.px = -50
            self.py = 0
        elif n == '2':
            self.py = -50
            self.px = 0
        elif n == '1':
            self.py = 50
            self.px = 0
        elif n == '0':
            self.px = self.py = 0


# заставка конца игры после смерти
class End(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        # Выводим картинку о завершении игры
        self.image = pygame.image.load(os.path.join('data1', 'gameover.png'))
        self.rect = self.image.get_rect()


# заставка выигрыша
class Win(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        # Выводим картинку о завершении игры
        self.image = pygame.image.load(os.path.join('data1', 'win.jpg'))
        self.rect = self.image.get_rect()


# Класс Плиток
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)


# игрок
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.image.get_rect().move(tile_width * x + 15, tile_height * y + 5)


# закрытие игры
def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data1/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


# начальная заставка
def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (550, 500))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начало игры
        pygame.display.flip()
        pygame.time.Clock().tick(30)


# постройка уровня
def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('grass', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('wall1', x, y)
            elif level[y][x] == 'x':
                Tile('cross', x, y)
            elif level[y][x] == '^':
                Tile('trap', x, y)
            elif level[y][x] == 'p':
                Tile('grass', x, y)
                np = Player(x, y)
    return np, x, y


if __name__ == '__main__':
    pygame.display.set_caption("Бегущий в лабиринте")
    pygame.init()
    camera = Camera()
    running = True
    start_screen()
    a = 1
    level_map = load_level(flnam)
    player, max_x, max_y = generate_level(level_map)
    all_sprites.draw(screen)
    player_group.draw(screen)
    if a == 1:
        for i in all_sprites:
            r(i)
        for j in player_group:
            r(j)
        a = 0
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # проверка позиций игрока
                x, y = player.pos
                if event.key == pygame.K_UP:
                    if level_map[y - 1][x] != '#' and level_map[y - 1][x] != '@':
                        if level_map[y - 1][x] == '^':
                            hp -= 5
                        camera.ud('1')
                        player.move(x, y - 1)
                        for sprite in all_sprites:
                            camera.apply(sprite)
                elif event.key == pygame.K_DOWN:
                    if level_map[y + 1][x] != '#' and level_map[y + 1][x] != '@':
                        if level_map[y + 1][x] == '^':
                            hp -= 5
                        camera.ud('2')
                        player.move(x, y + 1)
                        for sprite in all_sprites:
                            camera.apply(sprite)
                elif event.key == pygame.K_RIGHT:
                    if level_map[y][x + 1] != '#' and level_map[y][x + 1] != '@':
                        if level_map[y][x + 1] == '^':
                            hp -= 5
                        camera.ud('3')
                        player.move(x + 1, y)
                        for sprite in all_sprites:
                            camera.apply(sprite)
                elif event.key == pygame.K_LEFT:
                    if level_map[y][x - 1] != '#' and level_map[y][x - 1] != '@':
                        if level_map[y][x - 1] == '^':
                            hp -= 5
                        camera.ud('4')
                        player.move(x - 1, y)
                        for sprite in all_sprites:
                            camera.apply(sprite)
                        if level_map[y - 1][x] == '^':
                            hp -= 5
                            print(hp)
                else:
                    camera.ud('0')
            screen.fill((0, 0, 0))
            # проверка конца игры
            if (player.pos[0] == 1 and player.pos[1] == 1) or hp == 0:
                screen = pygame.display.set_mode((600, 300))
                if player.pos[0] == 1 and player.pos[1] == 1:
                    Win(all_sprites)
                elif hp == 0:
                    End(all_sprites)
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN or \
                                event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                            running = False
                    all_sprites.draw(screen)
                    pygame.display.update()
            pygame.display.flip()
            # обновление спрайтов
            all_sprites.draw(screen)
            player_group.draw(screen)
            # вывод здоровья
            drawtext(screen, 'Здоровье: ' + str(int(hp)), 18, 65, 10)
            pygame.display.flip()
    terminate()
