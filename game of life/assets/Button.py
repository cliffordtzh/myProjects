import pygame

class Button:
    def __init__(self, pos, dimension, text, color, surface, hover = True):
        self.x = pos[0]
        self.y = pos[1]
        self.width, self.height = dimension[0], dimension[1]
        self.surface = surface
        self.color = color
        self.font = pygame.font.SysFont("Helvetica", 18)
        self.font.bold = True
        self.text = self.font.render(text, False, (0, 0, 0))
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.hover = hover
        self.hovering = None
        self.hover_color = (255, 255, 255)

    def update(self, mouse_pos):
        self.rect.topleft = (self.x, self.y)
        self.hovering = self.mouse_over(mouse_pos)
 
    def draw(self, mouse_pos):
        text_pos = self.text.get_rect(center = self.image.get_rect().center)
        self.image.fill(self.color)
        if self.hover and self.hovering:
            border_width = 5
            pygame.draw.rect(self.image, self.hover_color, \
                [border_width, border_width, self.width-(2*border_width), self.height-(2*border_width)])
        self.image.blit(self.text, text_pos)
        self.surface.blit(self.image, (self.x, self.y))

    def mouse_over(self, mouse_pos):
        x, y = mouse_pos
        return self.x < x < self.x + self.width and \
            self.y < y < self.y + self.height
