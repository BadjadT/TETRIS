import pygame as pg
import sys
from pygame.locals import *

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


def start_game():
    pass


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
