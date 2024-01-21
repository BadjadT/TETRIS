import pygame as pg
import random
import sys
import time
from pygame.locals import *

# ОСНОВНЫЕ ПЕРЕМЕННЫЕ
WIDTH, HEIGHT = 600, 500
cell = 20
game_height, game_width = 20, 10

side_speed, down_speed = 0.15, 0.1

side_margin = int((WIDTH - game_width * cell) / 2)
top_margin = HEIGHT - (game_height * cell) - 5

fps = 25

block_col = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0), (221, 10, 178), (83, 218, 63), (0, 119, 211),
             (50, 255, 100), (255, 100, 100), (255, 255, 100))
base_colors = ((255, 255, 255), (0, 0, 0))

board_col, text_col = base_colors[0], base_colors[0]
title_col = block_col[3]
info_col = block_col[0]
bg_col = base_colors[1]

block_width, block_height = 5, 5
empty = 'o'


def main():
    global fps_clock, head_text, screen, normal_text
    pg.init()
    pg.display.set_caption("TETRIS")
    fps_clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    head_text = pg.font.SysFont('arial', 55)
    normal_text = pg.font.SysFont('arial', 20)
    start_image('tetris_back.jpg')
    while True:
        start_game()
        pause_scr()
        cen_text('GAME OVER')

# ЭКРАН ПАУЗЫ/ПРОИГРЫША
def pause_scr():
    pause = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    pause.fill((120, 120, 120, 150))
    screen.blit(pause, (0, 0))


# ВСЕ ФОРМЫ И их ВАРИАЦИИ
shapes = {1: [['ooooo',
               'ooooo',
               'oxxoo',
               'oxxoo',
               'ooooo']],
          2: [['ooxoo',
               'ooxoo',
               'ooxoo',
               'ooxoo',
               'ooooo'],
              ['ooooo',
               'ooooo',
               'xxxxo',
               'ooooo',
               'ooooo']],
          3: [['ooooo',
               'ooooo',
               'oxxoo',
               'ooxxo',
               'ooooo'],
              ['ooooo',
               'ooxoo',
               'oxxoo',
               'oxooo',
               'ooooo']],
          4: [['ooooo',
               'ooooo',
               'ooxxo',
               'oxxoo',
               'ooooo'],
              ['ooooo',
               'ooxoo',
               'ooxxo',
               'oooxo',
               'ooooo']],
          5: [['ooooo',
               'ooxoo',
               'oxxxo',
               'ooooo',
               'ooooo'],
              ['ooooo',
               'ooxoo',
               'ooxxo',
               'ooxoo',
               'ooooo'],
              ['ooooo',
               'ooooo',
               'oxxxo',
               'ooxoo',
               'ooooo'],
              ['ooooo',
               'ooxoo',
               'oxxoo',
               'ooxoo',
               'ooooo']],
          6: [['ooooo',
               'oxooo',
               'oxxxo',
               'ooooo',
               'ooooo'],
              ['ooooo',
               'ooxxo',
               'ooxoo',
               'ooxoo',
               'ooooo'],
              ['ooooo',
               'ooooo',
               'oxxxo',
               'oooxo',
               'ooooo'],
              ['ooooo',
               'ooxoo',
               'ooxoo',
               'oxxoo',
               'ooooo']],
          7: [['ooooo',
               'oooxo',
               'oxxxo',
               'ooooo',
               'ooooo'],
              ['ooooo',
               'ooxoo',
               'ooxoo',
               'ooxxo',
               'ooooo'],
              ['ooooo',
               'ooooo',
               'oxxxo',
               'oxooo',
               'ooooo'],
              ['ooooo',
               'oxxoo',
               'ooxoo',
               'ooxoo',
               'ooooo']]
          }


# ОСНОВНАЯ ИГРА
def start_game():
    game = empty_game()
    points = 0
    level, fall_speed = game_speed(points)
    go_down = False
    go_left = False
    go_right = False
    curr_block = get_block()
    next_block = get_block()
    latest_key_down = time.time()
    latest_key_side = time.time()
    latest_down = time.time()

    while True:
        if curr_block is None:
            curr_block = next_block
            next_block = get_block()
            latest_down = time.time()

            if not check(game, curr_block):
                return
        exit_game()
        for event in pg.event.get():
            if event.type == KEYUP:
                if event.key == K_p:
                    pause_scr()
                    cen_text('Pause')
                    latest_down = time.time()
                    latest_key_down = time.time()
                    latest_key_side = time.time()
                elif event.key == K_DOWN:
                    go_down = False
                elif event.key == K_RIGHT:
                    go_right = False
                elif event.key == K_LEFT:
                    go_left = False

            elif event.type == KEYDOWN:
                if event.key == K_LEFT and check(game, curr_block, new_x=-1):
                    curr_block['x'] -= 1
                    go_left = True
                    go_right = False
                    latest_key_side = time.time()

                elif event.key == K_RIGHT and check(game, curr_block, new_x=1):
                    curr_block['x'] += 1
                    go_right = True
                    go_left = False
                    latest_key_side = time.time()

                elif event.key == K_UP:
                    curr_block['variation'] = (curr_block['variation'] + 1) % len(shapes[curr_block['shape']])
                    if not check(game, curr_block):
                        curr_block['variation'] = (curr_block['variation'] - 1) % len(shapes[curr_block['shape']])

                elif event.key == K_DOWN:
                    if check(game, curr_block, new_y=1):
                        curr_block['y'] += 1
                    go_down = True
                    latest_key_down = time.time()

                elif event.key == K_SPACE:
                    for i in range(1, game_height):
                        if not check(game, curr_block, new_y=i):
                            break
                    curr_block['y'] += i - 1
                    go_down = False
                    go_left = False
                    go_right = False

        # УДЕРЖАНИЕ КЛАВИШИ
        if (go_left or go_right) and time.time() - latest_key_side > side_speed:
            if go_left and check(game, curr_block, new_x=-1):
                curr_block['x'] -= 1
            elif go_right and check(game, curr_block, new_x=1):
                curr_block['x'] += 1
            latest_key_side = time.time()

        if go_down and time.time() - latest_key_down > down_speed and check(game, curr_block, new_y=1):
            curr_block['y'] += 1
            latest_key_down = time.time()

        # СВОБОДНОЕ ПАДЕНИЕ
        if time.time() - latest_down > fall_speed:
            if not check(game, curr_block, new_y=1):
                add_block(game, curr_block)
                points += clear_full(game)
                level, fall_speed = game_speed(points)
                curr_block = None
            else:
                curr_block['y'] += 1
                latest_down = time.time()

        screen.fill(bg_col)
        gamecup(game)
        score_info(points, level)
        draw_nblock(next_block)
        if curr_block is not None:
            draw_block(curr_block)
        pg.display.update()
        fps_clock.tick(fps)


# НАЧАЛЬНЫЙ ЭКРАН
def start_image(image):
    start_img = pg.image.load(image)
    start_size = pg.transform.scale(start_img, (WIDTH, HEIGHT))
    screen.blit(start_size, (0, 0))

    while check_press() is None:
        pg.display.update()
        fps_clock.tick()


# ТЕКСТ ПРИ ПРОИГРЫШЕ/ПАУЗЕ
def cen_text(text):
    text_surf, text_rect = text_opt(text, head_text, title_col)
    text_rect.center = (int(WIDTH / 2) - 3, int(HEIGHT / 2) - 3)
    screen.blit(text_surf, text_rect)

    while check_press() is None:
        pg.display.update()
        fps_clock.tick()


# ПРОВЕРКА НАЖАТИЯ НА ЛЮБУЮ КЛАВИШУ
def check_press():
    exit_game()

    for event in pg.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


# УСЛОВИЯ ВЫХОДА ИЗ ИГРЫ
def exit_game():
    for _ in pg.event.get(QUIT):
        game_over()
    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            game_over()
        pg.event.post(event)


# ВЫХОД ИЗ ИГРЫ
def game_over():
    pg.quit()
    sys.exit()


def text_opt(text, font, color):
    screen = font.render(text, True, color)
    return screen, screen.get_rect()


# ОПУСТОШЕНИЕ ИГРОВОГО ПОЛЯ
def empty_game():
    game = []
    for i in range(game_width):
        game.append([empty] * game_height)
    return game


# ПОЛУЧЕНИЕ НОВОЙ ФИГУРЫ
def get_block():
    shape = random.choice(list(shapes.keys()))
    new_block = {'shape': shape,
                 'variation': random.randint(0, len(shapes[shape]) - 1),
                 'x': int(game_width / 2) - int(block_width / 2),
                 'y': -2,
                 'color': random.randint(0, len(block_col) - 1)}
    return new_block


# УРОВЕНЬ И СКОРОСТЬ ИГРЫ
def game_speed(points):
    level = int(points // 5)
    fall_speed = 0.5 - (level * 0.03)
    return level, fall_speed


# ОТРИСОВКА ИГРОВОГО ПОЛЯ
def gamecup(game):
    pg.draw.rect(screen, board_col,
                 (side_margin - 4, top_margin - 3, (game_width * cell) + 8, (game_height * cell) + 8),
                 5)

    pg.draw.rect(screen, bg_col, (side_margin, top_margin, cell * game_width, cell * game_height))
    for x in range(game_width):
        for y in range(game_height):
            draw_cell(x, y, game[x][y])


# ПРОВЕРКА СТОЛКНОВЕНИЙ
def check(game, block, new_x=0, new_y=0):
    for x in range(block_width):
        for y in range(block_height):
            not_in_game = y + block['y'] + new_y < 0
            if not_in_game or shapes[block['shape']][block['variation']][y][x] == empty:
                continue
            if not in_game((x + block['x'] + new_x), (y + block['y'] + new_y)):
                return False
            if game[x + block['x'] + new_x][y + block['y'] + new_y] != empty:
                return False
    return True


def in_game(x, y):
    return 0 <= x < game_width and y < game_height


# ОТРИСОВКА ОДНОЙ КЛЕТКИ
def draw_cell(block_x, block_y, color, pixel_x=None, pixel_y=None):
    if color == empty:
        return
    if pixel_x is None and pixel_y is None:
        pixel_x, pixel_y = surf_cord(block_x, block_y)
    pg.draw.rect(screen, block_col[color], (pixel_x + 1, pixel_y + 1, cell - 1, cell - 1))


# ОТРИСОВКА ВСЕЙ ФИГУРЫ
def draw_block(block, pixel_x=None, pixel_y=None):
    dr_block = shapes[block['shape']][block['variation']]
    if pixel_x is None and pixel_y is None:
        pixel_x, pixel_y = surf_cord(block['x'], block['y'])

    for x in range(block_width):
        for y in range(block_height):
            if dr_block[y][x] != empty:
                draw_cell(None, None, block['color'],
                          pixel_x + (x * cell), pixel_y + (y * cell))


def surf_cord(block_x, block_y):
    return (side_margin + (block_x * cell)), (top_margin + (block_y * cell))


# ОТРИСОВКА СЛЕДУЮЩЕЙ ФИГУРЫ
def draw_nblock(block):
    next_info = normal_text.render('NEXT:', True, text_col)
    text_rect = next_info.get_rect()
    text_rect.topleft = (WIDTH - 150, 180)
    screen.blit(next_info, text_rect)
    draw_block(block, pixel_x=WIDTH - 170, pixel_y=210)


# ДОБАВЛЕНИЕ ФИГУРЫ НА ИГРОВОЕ ПОЛЕ
def add_block(game, block):
    for x in range(block_width):
        for y in range(block_height):
            if shapes[block['shape']][block['variation']][y][x] != empty:
                game[x + block['x']][y + block['y']] = block['color']


# ПРОВЕРКА ПОЛНЫХ ЛИНИЙ
def full_check(game, y):
    for x in range(game_width):
        if game[x][y] == empty:
            return False
    return True


# ОЧИСТКА ПОЛНЫХ ЛИНИЙ И ИХ ПОДСЧЕТ ДЛЯ ДОБАВЛЕНИЯ ОЧКОВ
def clear_full(game):
    removed_lines = 0
    y = game_height - 1
    while y >= 0:
        if full_check(game, y):
            for i in range(y, 0, -1):
                for x in range(game_width):
                    game[x][i] = game[x][i - 1]
            for x in range(game_width):
                game[x][0] = empty
            removed_lines += 1
        else:
            y -= 1
    return removed_lines


# ПОКАЗ ИНФОРМАЦИИ О ОЧКАХ И УРОВНЕ ИГРЫ
def score_info(points, level):
    points_info = normal_text.render(f'SCORE: {points}', True, text_col)
    points_rect = points_info.get_rect()
    points_rect.topleft = (WIDTH - 550, 180)
    screen.blit(points_info, points_rect)

    level_info = normal_text.render(f'LEVEL: {level}', True, text_col)
    level_rect = level_info.get_rect()
    level_rect.topleft = (WIDTH - 550, 250)
    screen.blit(level_info, level_rect)


if __name__ == '__main__':
    main()
