import pygame
import random

class Cell:
    def __init__(self, pos, surface):
        self.alive = False
        self.x = pos[0]
        self.y = pos[1]
        self.surface = surface
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.neighbours = []

    def update(self):
        self.rect.topleft = (self.x*20, self.y*20)

    def draw(self):
        self.image.fill((0, 0, 0))
        if not self.alive:
            pygame.draw.rect(self.image, (255, 255, 255), [1, 1, 18, 18])
        self.surface.blit(self.image, (self.x*20, self.y*20)) 