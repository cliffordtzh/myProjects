try:
    from assets.Grid import Grid
    from assets.Button import Button
except ModuleNotFoundError:
    from Grid import Grid
    from Button import Button

import pygame
from pygame.locals import *
import numpy as np
import random

class Board:
    def __init__(self, s_mid, dimensions):
        self.width, self.height = dimensions
        self.s_width, self.s_height = s_mid

        self.x = self.s_width - (self.width/2)
        self.y = 1.15 * (self.s_height - (self.height/2))

        self.image = pygame.Surface(dimensions)
        
        self.grid = [
            [Grid(
                (ix, iy),
                (self.x, self.y),
                (self.width/9, self.height/9)
            ) for ix in range(9)]
            for iy in range(9)
        ]

    def draw_borders(self, screen):
        start_points = [
            (x, 0) for x in np.arange(0, self.width, self.width/9)
        ]

        end_points = [
            (x, self.height) for x in np.arange(0, self.width, self.width/9)
        ]

        pygame.draw.rect(
            self.image, (0, 0, 0), (0, 0, self.width, self.height), width = 2
        )

        for i, ((x1, y1), (x2, y2)) in enumerate(zip(start_points, end_points)):
            width = 2 if (i+1)%3 == 1 else 1
            pygame.draw.line(
                self.image, (0, 0, 0), (x1, y1), (x2, y2), width = width
            )

            pygame.draw.line(
                self.image, (0, 0, 0), (y1, x1), (y2, x2), width = width
            )

    def draw(self, screen):
        self.image.fill((255, 255, 255))
        for row in self.grid:
            for grid in row:
                grid.draw(self.image)

        self.draw_borders(screen)
        screen.blit(self.image, (self.x, self.y))

    def get(self, y, x):
        return self.grid[y][x].value

    def get_poss(self, y, x):
        nine_dir = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        sqr_y, sqr_x = int(y/3), (x//3)%3
        cy, cx = sqr_y*3 + 1, sqr_x*3 + 1
        dy, dx = y - cy, x - cx
        idx = (dy+1)*3 + dx + 1

        row = self.grid[y].copy()
        col = list(map(lambda row: row.copy()[x], self.grid))
        sqr = [self.grid[cy + i][cx + j] for i, j in nine_dir]

        row.pop(x), col.pop(y), sqr.pop(idx)
        return list(map(lambda grid: grid.value, row + col + sqr))

    def get_entropy(self, y, x):
        vals = set(filter(lambda x: x != None, self.get_poss(y, x)))
        return 9 - len(set(vals)), {i for i in range(1, 10)} - vals

    def update(self):
        for y, row in enumerate(self.grid):
            for x, grid in enumerate(row):
                entropy, vals = self.get_entropy(y, x)
                grid.update(entropy, vals)
        self.update_entropy()

    def update_entropy(self):
        for row in range(9):
            for col in range(9):
                entropy, vals = self.get_entropy(row, col)
                self.grid[row][col].entropy = entropy
                self.grid[row][col].entropy_vals = vals

    def is_possible(self, y, x, n):
        if self.get(y, x) is not None:
            return False

        if n in self.get_poss(y, x):
            return False

        return True

    def refresh(self):
        for row in self.grid:
            for grid in row:
                grid.value = None
                grid.collapsed = False
                grid.color = (255, 255, 255)

        self.update_entropy()

    def reset(self):
        for y, row in enumerate(self.grid):
            for x, grid in enumerate(row):
                if grid.color != (210, 210, 210):
                    entropy, vals = self.get_entropy(y, x)
                    grid.uncollapse(entropy, vals)
        

    def random_board(self, n):
        self.refresh()

        placed = 0
        while placed < n:
            choice = random.randint(0, 80)
            num_choice = random.randint(1, 9)

            y, x = int(choice/9), choice%9
            if self.is_possible(y, x, num_choice):
                self.grid[y][x].collapse(num_choice, user = True)
                placed += 1

        self.update_entropy()

    def set_value(self, pos, value):
        y, x = pos
        self.grid[y][x].collapse(value)

    def set_board(self, poss, values):
        for p, v in zip(poss, values):
            self.set_value(p, v)

    def uncollapse(self, pos):
        y, x = pos
        entropy = self.get_entropy(y, x)
        entropy, vals = self.get_entropy(y, x)
        self.grid[y][x].uncollapse(entropy, vals)

    def simplify(self):
        return [
            [self.grid[x][y].value if self.grid[x][y].value is not None else 0 for y in range(9)]
            for x in range(9)
        ]

    def get_min_entropy(self):
        smallest = 9
        res = None, None
        for row in range(9):
            for col in range(9):
                grid = self.grid[row][col]
                if grid.collapsed:
                    continue

                if grid.entropy < smallest:
                    smallest = grid.entropy
                    res = ((row, col), grid)

        return res

    @staticmethod
    def print(grid):
        indent = "    "
        for i, row in enumerate(grid):
            res = indent + "|["
            for j, grid in enumerate(row):
                val = "-" if grid.value is None else str(grid.value)
                res += val
                if j == len(row) - 1:
                    res += "]|"
                elif (j+1)%3 == 0:
                    res += "]["
                else:
                    res += " "
            if (i)%3 == 0:
                print(indent + f"|{'-' * (len(res)-6)}|")
            print(res)
        print(indent + f"|{'-' * (len(res)-6)}|")
        print("\n")

    def __str__(self):
        return str([
            list(map(lambda x: x.value, row))
            for row in self.grid
        ])

    def __repr__(self):
        return self.__str__()
        