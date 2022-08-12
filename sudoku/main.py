from assets.Board import Board
from assets.Button import Button, G_Button
from assets.Solver import Solver

import pygame
from pygame.locals import *
import numpy as np
import time

DIM = (900, 900)
BACKGROUND = (255, 255, 255)
RUN = True

pygame.init()
screen = pygame.display.set_mode(DIM)
background = pygame.Surface(DIM)
background.fill(BACKGROUND)

screen_center = screen.get_rect().center
board = Board(screen_center, (540, 540))
board.random_board(15)
text = pygame.font.SysFont("Arial", 31)

button_args = {
    "dimensions": (140, 50),
    "color": (100, 100, 100),
    "text_size": 14,
    "text_color": (0, 0, 0),
    "hover": True,
    "hover_color": (120, 10, 120)
}

solve1_button = Button(**button_args, pos = (220, 57), val = "Entropy Solve")
solve2_button = Button(**button_args, pos = (380, 57), val = "Solve")
random_button = Button(**button_args, pos = (540, 57), val = "Random")
stop_button = Button(**button_args, pos = (220, 132), val = "Stop")
reset_button = Button(**button_args, pos = (380, 132), val = "Reset")
refresh_button = Button(**button_args, pos = (540, 132), val = "Refresh")

buttons = [solve1_button, solve2_button, refresh_button, random_button, stop_button, reset_button]

solver = Solver(board, screen, background, stop_button)

for button in buttons:
    button.draw(screen)
board.draw(screen)


def update_game(screen, buttons, background, solved):
    screen.blit(background, (0, 0))
    for button in buttons:
        button.draw(screen)
    board.draw(screen)

    if solved is not None:
        if solved:
            rendered = text.render("SOLVED", True, (90, 158, 112))
            screen.blit(rendered, (400, 750))
        else:
            rendered = text.render("UNSOLVED", True, (220, 120, 0))
            screen.blit(rendered, (380, 750))

    pygame.display.flip()

solved = None
while RUN:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            RUN = False
        if event.type == MOUSEBUTTONDOWN:
            if solve1_button.hovering():
                try:
                    solved = solver.ent_solve(buttons)
                except ValueError:
                    solved = False

            if solve2_button.hovering():
                try:
                    solved = solver.solve(buttons)
                except ValueError:
                    solved = False

            if refresh_button.hovering():
                board.refresh()
            if random_button.hovering():
                board.random_board(15)
            if reset_button.hovering():
                board.reset()

            board.update()

    update_game(screen, buttons, background, solved)