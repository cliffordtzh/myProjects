import pygame
from pygame.locals import *

class Solver:
    def __init__(self, board, screen, background, stop_button):
        self.board = board
        self.screen = screen
        self.background = background
        self.stop = stop_button

    def update_game(self, buttons):
        self.screen.blit(self.background, (0, 0))
        for button in buttons:
            button.draw(self.screen)
        self.board.draw(self.screen)
        pygame.display.flip()

    def solve(self, buttons, show = True):
        for x in range(9):
            for y in range(9):
                if self.board.get(y, x) is not None:
                    continue
                
                for n in range(1, 10):
                    if self.board.is_possible(y, x, n):
                        self.board.set_value((y, x), n)

                        if show:
                            self.update_game(buttons)
                            for event in pygame.event.get():
                                if event.type == MOUSEBUTTONDOWN and self.stop.hovering():
                                    raise ValueError

                        if self.solve(buttons):
                            return True
                        else:
                            self.board.uncollapse((y, x))

                return False
        return True

    def ent_solve(self, buttons, show = True):
        pos, grid = self.board.get_min_entropy()
        if grid is None:
            return True

        y, x = pos
        poss = grid.entropy_vals

        for value in poss:
            self.board.grid[y][x].collapse(value)
            self.board.update_entropy()

            if show:
                self.update_game(buttons)
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN and self.stop.hovering():
                        raise ValueError
            
            if self.ent_solve(buttons):
                return True
            else:
                self.board.uncollapse(pos)

        return False