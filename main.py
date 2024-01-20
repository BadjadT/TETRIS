import pygame as pg
import random
import sys
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
colors = ((255, 255, 255), (0, 0, 0))

board_col, text_col = colors[0], colors[0]
title_col = block_col[3]
info_col = block_col[0]
bg_col = colors[1]

block_width, block_height = 5, 5
empty = 'o'


def main():
    global fps_clock, head_text, surf
    pg.init()
    pg.display.set_caption("TETRIS")
    fps_clock = pg.time.Clock()
    surf = pg.display.set_mode((WIDTH, HEIGHT))
    head_text = pg.font.SysFont('arial', 55)
    cen_text('TETRIS')
    while True:
        start_game()
        pause_scr()
        cen_text('GAME OVER')


def pause_scr():
    pause = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    pause.fill((120, 120, 120, 150))
    surf.blit(pause, (0, 0))


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


def start_game():
    game = empty_game()
    points = 0
    level = game_level(points)
    fall_speed = game_speed(level)
    go_down = False
    go_left = False
    go_right = False
    curr_block = get_block()
    next_block = get_block()
    while True:
        if curr_block is None:
            curr_block = next_block
            next_block = get_block()

            if not check(game, curr_block):
                return
        exit_game()
        for event in pg.event.get():
            if event.type == KEYUP:
                if event.key == K_p:
                    pause_scr()
                    cen_text('Pause')

            elif event.type == KEYDOWN:
                if event.key == K_LEFT and check(game, curr_block, new_x=-1):
                    curr_block['x'] -= 1

                elif event.key == K_RIGHT and check(game, curr_block, new_x=1):
                    curr_block['x'] += 1

                elif event.key == K_UP:
                    curr_block['variation'] = (curr_block['variation'] + 1) % len(shapes[curr_block['shape']])
                    if not check(game, curr_block):
                        curr_block['variation'] = (curr_block['variation'] - 1) % len(shapes[curr_block['shape']])

                elif event.key == K_DOWN:
                    if check(game, curr_block, new_y=1):
                        curr_block['y'] += 1

                elif event.key == K_SPACE:
                    for i in range(1, game_height):
                        if not check(game, curr_block, new_y=i):
                            break
                    curr_block['y'] += i - 1


def cen_text(text):
    text_surf, text_rect = text_opt(text, head_text, title_col)
    text_rect.center = (int(WIDTH / 2) - 3, int(HEIGHT / 2) - 3)
    surf.blit(text_surf, text_rect)

    while check_press() is None:
        pg.display.update()
        fps_clock.tick()


def check_press():
    exit_game()

    for event in pg.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def exit_game():
    for _ in pg.event.get(QUIT):
        game_over()
    for event in pg.event.get(KEYUP):
        if event.key == K_ESCAPE:
            game_over()
        pg.event.post(event)


def game_over():
    pg.quit()
    sys.exit()


def text_opt(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def empty_game():
    game = []
    for i in range(game_width):
        game.append([empty] * game_height)
    return game


def get_block():
    shape = random.choice(list(shapes.keys()))
    new_block = {'shape': shape,
                 'variation': random.randint(0, len(shapes[shape]) - 1),
                 'x': int(game_width / 2) - int(block_width / 2),
                 'y': -2,
                 'color': random.randint(0, len(block_col) - 1)}
    return new_block


def game_level(points):
    level = 0
    return level


def game_speed(level):
    pass


def check(game, block, new_x=0, new_y=0):
    for x in range(block_width):
        for y in range(block_height):
            not_in_game = y + block['y'] + new_y < 0
            if not_in_game or shapes[block['shape']][block['variation']][y][x] == empty:
                continue
            if not 0 <= (x + block['x'] + new_x) < game_width and (y + block['y'] + new_y) < game_height:
                return False
            if game[x + block['x'] + new_x][y + block['y'] + new_y] != empty:
                return False
    return True


if __name__ == '__main__':
    main()
