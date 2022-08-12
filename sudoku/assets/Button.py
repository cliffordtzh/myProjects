import pygame
from pygame.locals import *

class Button:
    def __init__(self, pos, dimensions, color, val, text_size, text_color, hover = False, hover_color = None):
        self.x, self.y = pos
        self.width, self.height = dimensions
        self.val = val
        self.text_color = text_color
        self.color = color
        self.hover = hover
        self.hover_color = hover_color

        self.image = pygame.Surface(dimensions)
        self.font = pygame.font.SysFont('Arial', text_size)

    def draw(self, surface):
        self.image.fill(self.color)
        if self.hover and self.hovering():
            pygame.draw.rect(
                self.image,
                self.hover_color,
                (0, 0, self.width, self.height)
            )
        
        text = self.font.render(self.val, True, self.text_color)
        center = text.get_rect(center = (self.width/2, self.height/2))

        self.image.blit(text, center)
        surface.blit(self.image, (self.x, self.y))

    def hovering(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        return (
            self.x < mouse_x < self.x + self.width
        ) and (
            self.y < mouse_y < self.y + self.height
        )


class G_Button(Button):
    def __init__(self, p_pos, dimensions, color, val, text_size, text_color, hover = False, hover_color = None):

        super().__init__(
            p_pos, dimensions, color, val, text_size, 
            text_color, hover, hover_color
        )

        i = int(val) - 1
        self.px, self.py = p_pos
        self.width, self.height = dimensions
        self.ix, self.iy = i%3, int(i/3)
        self.x, self.y = self.px + (self.width * self.ix), self.py + (self.height * self.iy)
        self.rx, self.ry = (self.width * self.ix), (self.height * self.iy)

    def draw(self, surface):
        self.image.fill(self.color)
        if self.hover and self.hovering():
            pygame.draw.rect(
                self.image,
                self.hover_color,
                (0, 0, self.width, self.height)
            )
        
        text = self.font.render(str(self.val), True, self.text_color)
        center = text.get_rect(center = (self.width/2, self.height/2))

        self.image.blit(text, center)
        surface.blit(self.image, (self.rx, self.ry))
