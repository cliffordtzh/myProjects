try:
    from assets.Button import Button, G_Button
except ModuleNotFoundError:
    from Button import Button, G_Button

import pygame
from pygame.locals import *
import numpy as np


class Grid:
    def __init__(self, i, p_pos, dimensions):
        self.ix, self.iy = i
        self.width, self.height = dimensions
        self.px, self.py = p_pos
        self.x, self.y = self.px + (self.ix * self.width), self.py + (self.iy * self.height)
        self.rx, self.ry = self.ix * self.width, self.iy * self.height
        self.collapsed = False
        self.value = None
        self.color = (255, 255, 255)
        self.entropy_vals = {i for i in range(1, 10)}
        self.entropy = 9

        self.image = pygame.Surface(dimensions)
        self.font = pygame.font.SysFont('Arial', 31)

        button_args = {
            "p_pos": (self.x, self.y),
            "dimensions": (self.width/3, self.height/3),
            "color": (255, 255, 255),
            "text_size": 11,
            "text_color": (0, 0, 0),
            "hover": True,
            "hover_color": (200, 200, 110)
        }

        self.grid = [
            [G_Button(
                **button_args,
                val = i + j*3 + 1,
                ) for i in range(3)]
            for j in range(3)
        ]

    def update(self, entropy, vals):
        for row in self.grid:
            for button in row:
                if button.hovering() and not self.collapsed:
                    self.collapse(button.val, user = True)
                elif button.hovering() and self.collapsed:
                    self.uncollapse(entropy, vals)

    def draw(self, screen):
        if not self.collapsed:
            self.image.fill(self.color)
            for row in self.grid:
                for button in row:
                    if button.val in self.entropy_vals:
                        button.draw(self.image)
            
        else:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(self.color)

            text = self.font.render(str(self.value), True, (0, 0, 0))
            center = text.get_rect(center = (self.width/2, self.height/2))
            self.image.blit(text, center)

        screen.blit(self.image, (self.rx, self.ry))

    def collapse(self, val, user = False):
        self.entropy = None
        self.entropy_vals = {}
        self.collapsed = True
        self.value = int(val)
        if user:
            self.color = (210, 210, 210)

    def uncollapse(self, entropy, vals):
        self.collapsed = False
        self.value = None
        self.entropy = entropy
        self.entropy_vals = vals
        self.color = (255, 255, 255)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


def main():
    DIM = (540, 540)
    BACKGROUND = (255, 255, 255)
    RUN = True

    pygame.init()
    screen = pygame.display.set_mode(DIM)
    background = pygame.Surface(DIM)
    background.fill(BACKGROUND)

    grid = [
        [Grid((x, y), (DIM[0]/9, DIM[1]/9)) for x in np.arange(0, DIM[0], DIM[0]/9)]
        for y in np.arange(0, DIM[1], DIM[1]/9)
    ]

    for row in grid:
        for g in row:
            g.draw(screen)

    while RUN:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                RUN = False
            if event.type == MOUSEBUTTONDOWN:
                for row in grid:
                    for g in row:
                        g.update(pygame.mouse.get_pos())

        for row in grid:
            for g in row:
                g.draw(screen)

        pygame.display.flip()
        
if __name__ == '__main__':
    main()