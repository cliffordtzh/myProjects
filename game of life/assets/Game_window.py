import pygame
from assets.Cell import Cell

vec = pygame.math.Vector2

class Game_window:
    def __init__(self, screen, x, y, infinite = False):
        self.screen = screen
        self.pos = vec(x, y)
        self.height, self.width = 600, 600
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rows = 30
        self.cols = 30
        self.grid = [[Cell((x, y), self.image) for y in range(self.cols)] for x in range(self.rows)]
        self.last_grid = None
        self.infinite = infinite

    def find_neighbours(self, pos):
        res = []
        neighbours = [
            (0, 1), (0, -1), (1, 0), (1, 1), 
            (1, -1), (-1, 0), (-1, 1), (-1, -1)
        ]

        for neighbour in neighbours:
            x, y = pos
            dx, dy = neighbour
            x += dx
            y += dy

            if self.infinite:
                x = self.rows-1 if x < 0 else x
                x = 0 if x >= self.rows else x
                y = self.cols-1 if y < 0 else y
                y = 0 if y >= self.cols else y

            else:
                if not 0 <= x < self.rows or not 0 <= y < self.cols:
                    continue

            try:
                cell_grid = self.grid
                res.append(cell_grid[x][y].alive)
            except IndexError:
                print(x, y)

        return res

    def update(self):
        self.rect.topleft = self.pos
        for row in self.grid:
            for cell in row:
                cell.update()
                pos = (cell.x, cell.y)
                cell.neighbours = self.find_neighbours(pos)

    def draw(self):
        for row in self.grid:
            for cell in row:
                cell.draw()
        self.screen.blit(self.image, (self.pos.x, self.pos.y))

    def next_gen(self):
        next_grid = [[Cell((x, y), self.image) for y in range(self.cols)] for x in range(self.rows)]
        for row in range(self.rows):
            for col in range(self.cols):
                curr_cell = self.grid[row][col]
                next_cell = next_grid[row][col]
                total_neighbours = sum(curr_cell.neighbours)
                if curr_cell.alive:
                    if total_neighbours < 2 or total_neighbours > 3:
                        next_cell.alive = False
                    elif total_neighbours == 2 or total_neighbours == 3:
                        next_cell.alive = True
                else:
                    if total_neighbours == 3:
                        next_cell.alive = True
        
        self.grid = next_grid