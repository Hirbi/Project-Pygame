import pygame
import sys
import time
from random import choice


pygame.mixer.init()
FPS = 60
size = width, height = 500, 700
screen_rect = (0, 0, width, height)
pygame.init()
pygame.mouse.set_visible(0)
pygame.display.set_caption("Running thing!")
screen = pygame.display.set_mode(size, 0, 0)
finish_rect = None
Dead_Screen = False
WATER_EGG = False
gameIcon = pygame.image.load('data\\icon.png')
pygame.display.set_icon(gameIcon)
tile_images = {'grass': pygame.image.load('data\\grass.jpg'),
               'road': pygame.image.load('data\\road.jpg'),
               'finish': pygame.image.load('data\\finish.jpg'),
               'water': pygame.image.load('data\\water.jpg'),
               'wood': pygame.image.load('data\\wood.jpg'),
               'railway': pygame.image.load('data\\railway.png'),
               'train': pygame.image.load('data\\train.png'),
               'tree': pygame.image.load('data\\tree.png'),
               'stone': pygame.image.load('data\\stone.png')}

persons = ['mar.png', 'clown.png', 'dino.png']
NUMBER_OF_PERS = 0
DIFFICULTY = 1
BLOCKS = 25
VOLUME = 0.2
jump = pygame.mixer.Sound('data\\snd\\jump.wav')
gameover_music = pygame.mixer.Sound('data\\snd\\game_over.wav')
victory_music = pygame.mixer.Sound('data\\snd\\victory.wav')
pygame.mixer_music.set_volume(VOLUME)
jump.set_volume(VOLUME)
victory_music.set_volume(VOLUME)


class Objects(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(object_sprite, all_sprite)
        self.type = 'object'
        self.image = choice([tile_images['stone']] + [tile_images['tree']] * 4)
        self.rect = self.image.get_rect().move(pos[0], pos[1])


class Car(pygame.sprite.Sprite):
    images = [pygame.image.load('data\\car_taxi.png'), pygame.image.load('data\\car_police.png'),
              pygame.image.load('data\\car_sckoraya.png')]
    images += [pygame.image.load('data\\car_norm1.png'), pygame.image.load('data\\car_norm2.png')] * 3

    def __init__(self, pos):
        super().__init__(car_sprite, all_sprite)
        self.type = 'car'
        self.image = choice(self.images)
        self.rect = self.image.get_rect()
        self.pos = [pos[0], pos[1]]
        self.speed = 5
        self.v = self.speed + choice([0, 1, 2, 3])
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def update(self):
        if -120 <= self.rect.y < 820:
            if not self.rect.colliderect(screen_rect):
                self.v = self.speed + choice([0, 1, 2, 3])
                self.rect.x = self.pos[0]
                self.rect.y = self.pos[1]
                self.image = choice(self.images)
            self.rect = self.rect.move(-self.v, 0)


class Player(pygame.sprite.Sprite):

    def __init__(self, height, number_pers):
        super().__init__(player_sprite, all_sprite)
        self.image = pygame.image.load('data\\persons\\' + persons[number_pers])
        self.type = 'player'
        self.rect = self.image.get_rect().move(350, height)
        self.mask = pygame.mask.from_surface(self.image)
        self.dead_move_v = 0

    def update(self):
        global running, Dead_Screen
        if running:
            for sprite in tile_sprite:
                if self.rect.colliderect(sprite.rect) and sprite.type == 'water':
                    flag, napr = True, -1
                    for spritej in wood_sprite:
                        if spritej.rect.x <= self.rect.x \
                                and spritej.rect.x + spritej.rect.w >= self.rect.x + self.rect.w \
                                and abs(spritej.rect.y - self.rect.y) <= 20:
                            flag = False
                            napr = spritej.napr
                            break
                    if flag:
                        self.dead_move_v = 1000
                        Dead_Screen = True
                        running = False
                    else:
                        if napr:
                            self.rect = self.rect.move(-1, 0)
                        else:
                            self.rect = self.rect.move(1, 0)
            for sprite in car_sprite:
                if pygame.sprite.collide_mask(self, sprite):
                    running = False
                    self.dead_move_v = sprite.v
                    Dead_Screen = True
            for sprite in railway_sprite:
                if pygame.sprite.collide_mask(self, sprite):
                    running = False
                    self.dead_move_v = sprite.v
                    Dead_Screen = True
            if self.rect.colliderect(finish_rect):
                running = False
                Dead_Screen = False
                finish_screen()
        else:
            if self.rect.x > -50:
                self.rect.x -= self.dead_move_v // 2


def easter_egg():
    image = pygame.image.load("data\\fons\\easter_fon.png")
    screen.blit(image, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == 27:
                    return
                if event.key == 119:
                    global WATER_EGG
                    WATER_EGG = not WATER_EGG
                if event.key == 103:
                    global persons
                    if 'goose.png' not in persons:
                        persons.append('goose.png')
        screen.blit(image, (0, 0))
        pygame.display.flip()


def stop_game():
    image = pygame.image.load("data\\fons\\stop.png")
    screen.blit(image, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == 13:
                    return
                if event.key == 27:
                    return True
        screen.blit(image, (0, 0))
        pygame.display.flip()


def settings():
    global BLOCKS, VOLUME
    image = pygame.image.load("data\\fons\\settings.png")
    screen.blit(image, (0, 0))
    coords_blocks = {25: (128, 140), 50: (128, 240), 100: (128, 340), 200: (125, 440)}
    coords_dif = {1: (235, 250), 2: (335, 250), 3: (435, 250)}
    coords_sound = {0.2: (330, 550), 0: (330, 600)}
    image_cursor_blocks = pygame.image.load("data\\blocks.png")
    image_cursor_dif = pygame.image.load("data\\blocks.png")
    image_cursor_sound = pygame.image.load("data\\blocks.png")
    screen.blit(image_cursor_blocks, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                global DIFFICULTY
                if event.key == 27:
                    return
                if 49 <= event.key <= 52:
                    kolvo = [25, 50, 100, 200]
                    BLOCKS = kolvo[event.key - 49]
                if event.key == 113:
                    DIFFICULTY = 1
                if event.key == 119:
                    DIFFICULTY = 2
                if event.key == 101:
                    DIFFICULTY = 3
                if event.key == 118:
                    VOLUME = 0.2 - VOLUME
                if event.key == 96:
                    easter_egg()
        pygame.mixer_music.set_volume(VOLUME)
        jump.set_volume(VOLUME)
        victory_music.set_volume(VOLUME)
        screen.blit(image, (0, 0))
        screen.blit(image_cursor_blocks, coords_blocks[BLOCKS])
        screen.blit(image_cursor_dif, coords_dif[DIFFICULTY])
        screen.blit(image_cursor_sound, coords_sound[VOLUME])
        pygame.display.flip()


class Tiles(pygame.sprite.Sprite):
    def __init__(self, type, x, y, arg=0):
        if type == 'wood':
            self.napr = arg
            super().__init__(tile_sprite, all_sprite, wood_sprite)
        else:
            super().__init__(tile_sprite, all_sprite)
        self.type = type
        self.image = tile_images[type]
        self.rect = self.image.get_rect().move(x, y)

    def update(self, *args):
        if self.type == 'wood' and -120 <= self.rect.y < 820:
            if self.napr:
                self.rect.x = (self.rect.x - 1)
                if self.rect.x < -60:
                    self.rect.x += 700
            else:
                self.rect.x = (self.rect.x + 1)
                if self.rect.x > 700:
                    self.rect.x -= 740


class Train(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__(all_sprite, railway_sprite)
        self.image = tile_images[type]
        self.type = type
        self.rect = self.image.get_rect().move(x, y)
        self.per = choice(range(70, 125))
        self.v = 0
        self.sound = pygame.mixer.Sound('data\\snd\\train.wav')
        self.sound.set_volume(VOLUME / 4)
        self.last_time = 0

    def update(self, start_time=1):
        if -120 <= self.rect.y < 820:
            start_time = int((time.time() - start_time) * 100)
            if start_time != self.last_time and start_time % self.per == 0:
                self.last_time = start_time
                self.v = 20
            elif start_time % self.per == self.per - 30 and 0 < self.rect.y < 700 and running:
                self.sound.play()
            if self.rect.x < -700:
                self.sound.stop()
                self.rect.x = 700
                self.per += choice(range(270, 425))
                self.v = 0
            self.rect.x -= self.v


def generate_level():
    level_map = ['0'] * 15 + ['F']
    tiles = ['1', '1', '1', '1', 'W', 'W', 'R', 'R']
    lst = '0'
    global WATER_EGG
    if WATER_EGG:
        level_map = level_map + ['W1', 'W0'] * (BLOCKS // 2)
        if BLOCKS == 25:
            level_map.append('W1')
    else:
        for i in range(BLOCKS):
            if lst == '0':
                lst = choice(tiles)
                if lst == 'W':
                    lst = choice(['W1', 'W0'])
                level_map = level_map + [lst]
            else:
                if lst == 'W1':
                    napr = '0'
                else:
                    napr = '1'
                lst = choice([lst] * DIFFICULTY + ['0'] * (4 - DIFFICULTY))
                if lst[0] == 'W':
                    lst = lst[0] + napr
                level_map = level_map + [lst]

    level_map = level_map + ['@', '0', '0']
    return level_map


def make_back():
    level_map = generate_level()
    player = None
    for num, el in enumerate(level_map[::-1]):
        if el == '1':
            Tiles('road', 0, height - 50 - 60 * num)
            Car((width, height - 50 - 60 * num))
        elif el == '0':
            Tiles('grass', 0, height - 50 - 60 * num)
            Objects((choice(range(100)), height - 40 - 60 * num))
            Objects((choice(range(250, 350)), height - 40 - 60 * num))
            Objects((choice(range(500, 600)), height - 40 - 60 * num))
        elif el == '@':
            player = Player(height - 30 - 60 * num, NUMBER_OF_PERS)
            Tiles('grass', 0, height - 50 - 60 * num)
        elif el == 'F':
            global finish_rect
            finish_rect = Tiles('finish', 0, height - 50 - 60 * num).rect
        elif el[0] == 'W':
            Tiles('water', 0, height - 50 - 60 * num)
            napr = int(el[1])
            Tiles('wood', choice(range(-40, 60)), height - 30 - 60 * num, napr)
            Tiles('wood', choice(range(200, 300)), height - 30 - 60 * num, napr)
            Tiles('wood', choice(range(500, 600)), height - 30 - 60 * num, napr)
        elif el == 'R':
            Tiles('railway', 0, height - 50 - 60 * num)
            Train('train', 700, height - 50 - 60 * num)
    return player, level_map


class Camera:
    def __init__(self):
        self.tm = 0
        self.dx = 0
        self.dy = 0
        self.brk = False

    def apply(self, obj):
        if obj.type == 'car':
            obj.pos = (obj.pos[0], obj.pos[1] + self.dy)
        if obj.rect.x + self.dx >= -200:
            obj.rect.x += self.dx
        obj.rect.y += self.dy
        if self.tm % 2 == 0:
            obj.rect.y = obj.rect.y + 1
            if obj.type == 'car':
                obj.pos = (obj.pos[0], obj.pos[1] + 1)

    def update(self, target):
        self.tm += 1
        if target.rect.y < 250:
            self.dy = 50
        else:
            self.dy = 0
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        x, y = None, None
        for sprite in tile_sprite:
            x, y = sprite.rect.x, sprite.rect.y
        if y + self.dy > 0:
            self.dy = 0
        if y + 1 > 0:
            self.brk = True
        if self.dx < 0 and x <= -185:
            self.dx = 0
        if self.dx > 0 and x >= -25:
            self.dx = 0


def terminate():
    pygame.quit()
    sys.exit()


def finish_screen():
    pygame.mixer_music.stop()
    victory_music.play()
    image = pygame.image.load("data\\fons\\finished.png")
    screen.blit(image, (0, 0))
    for sprite in railway_sprite:
        sprite.sound.stop()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                victory_music.stop()
                return
        all_sprite.update()
        all_sprite.draw(screen)
        player_sprite.update()
        player_sprite.draw(screen)
        screen.blit(image, (0, 0))
        pygame.display.flip()


def start_screen():
    pygame.mixer_music.load('data\\snd\\music_menu.wav')
    pygame.mixer_music.play(-1)
    image = pygame.image.load("data\\fons\\mar.png")
    screen.blit(image, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                global NUMBER_OF_PERS
                if event.key == 13:
                    return
                if event.key == 275:
                    NUMBER_OF_PERS = (NUMBER_OF_PERS + 1) % len(persons)
                if event.key == 276:
                    NUMBER_OF_PERS = (NUMBER_OF_PERS - 1) % len(persons)
                if event.key == 27:
                    settings()
        image = pygame.image.load("data\\fons\\" + persons[NUMBER_OF_PERS])
        screen.blit(image, (0, 0))
        pygame.display.flip()


def dead_screen():
    gameover_music.play()
    image = pygame.image.load("data\\fons\\DeadFon2.png")
    screen.blit(image, (0, 0))
    for sprite in railway_sprite:
        sprite.sound.stop()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == 13:
                    gameover_music.stop()
                    return True
                elif event.key == 27:
                    gameover_music.stop()
                    return False
        all_sprite.update()
        all_sprite.draw(screen)
        player_sprite.update()
        player_sprite.draw(screen)
        screen.blit(image, (0, 0))
        pygame.display.flip()


def draw_info(player_step, start_time):
    if BLOCKS > 50:
        rect_width = 140
    else:
        rect_width = 100
    pygame.draw.rect(screen, (62, 180, 137), (5, 5, rect_width, 70))
    font = pygame.font.Font(None, 50)

    def to_string(int):
        if BLOCKS // 100:
            return str(int // 100) + str(int % 100 // 10) + str(int % 100 % 10)
        else:
            return str(int // 10) + str(int % 10)

    text = font.render(to_string(player_step) + "/" + to_string(BLOCKS), 1, (255, 222, 173))
    screen.blit(text, (10, 10))

    def make_time(ttime):
        if BLOCKS > 50:
            space = "  "
        else:
            space = ""
        return space + str(ttime // 60 // 10) + str(ttime // 60 % 10) + ":" \
               + str(ttime % 60 // 10) + str(ttime % 60 % 10)

    font = pygame.font.Font(None, 50)
    text = font.render(make_time(int(time.time() - start_time)), 1, (255, 222, 173))
    screen.blit(text, (10, 40))


def game():
    global Dead_Screen
    if Dead_Screen:
        Dead_Screen = dead_screen()
    if not Dead_Screen:
        start_screen()
    global all_sprite, tile_sprite, car_sprite, player_sprite, \
        running, wood_sprite, railway_sprite, object_sprite
    all_sprite = pygame.sprite.Group()
    object_sprite = pygame.sprite.Group()
    railway_sprite = pygame.sprite.Group()
    wood_sprite = pygame.sprite.Group()
    car_sprite = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    tile_sprite = pygame.sprite.Group()
    running = True
    clock = pygame.time.Clock()
    player, level = make_back()
    camera = Camera()
    start_time = time.time()
    player_step = 0
    pygame.mixer_music.load('data\\snd\\music.ogg')
    pygame.mixer_music.play(-1)
    while running:
        if player.rect.y > 650 or player.rect.y < 0 or player.rect.x < 0 or player.rect.x > 500:
            Dead_Screen = True
            break
        if not (-50 <= player.rect.x < width + 50):
            Dead_Screen = True
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                x, y = 0, 0
                if event.key == 27:
                    stop = stop_game()
                    if stop:
                        return
                if event.key == 275:
                    x, y = 25, 0
                    jump.play()
                elif event.key == 276:
                    x, y = -25, 0
                    jump.play()
                elif event.key == 273:
                    player_step += 1
                    x, y = 0, -60
                    jump.play()
                elif event.key == 274:
                    player_step -= 1
                    x, y = 0, 60
                    jump.play()
                step = True
                for sprite in object_sprite:
                    if sprite.rect.x <= player.rect.x + player.rect.w + x <= sprite.rect.x \
                            + sprite.rect.w and abs(sprite.rect.y - player.rect.y) < 20:
                        x -= player.rect.x + player.rect.w + x - sprite.rect.x + 1
                    elif sprite.rect.x <= player.rect.x + x <= sprite.rect.x \
                            + sprite.rect.w and abs(sprite.rect.y - player.rect.y) < 20:
                        x = sprite.rect.x + sprite.rect.w - player.rect.x + 1
                    elif sprite.rect.x <= player.rect.x + player.rect.w <= sprite.rect.x \
                            + sprite.rect.w and abs(sprite.rect.y - player.rect.y - y) < 20:
                        step = False
                    elif sprite.rect.x <= player.rect.x <= sprite.rect.x \
                            + sprite.rect.w and abs(sprite.rect.y - player.rect.y - y) < 20:
                        step = False
                if 0 <= player.rect.x + x < width and step:
                    player.rect = player.rect.move(x, y)
        screen.fill((62, 180, 137))
        camera.update(player)
        for sprite in all_sprite:
            camera.apply(sprite)
        tile_sprite.draw(screen)
        object_sprite.draw(screen)
        railway_sprite.draw(screen)
        player_sprite.update()
        player_sprite.draw(screen)
        car_sprite.update()
        car_sprite.draw(screen)
        wood_sprite.update()
        railway_sprite.update(start_time)
        draw_info(player_step, start_time)
        clock.tick(FPS)
        pygame.display.flip()
    return


def main():
    while True:
        game()


running = None
all_sprite = None
object_sprite = None
railway_sprite = None
wood_sprite = None
car_sprite = None
player_sprite = None
tile_sprite = None
main()
