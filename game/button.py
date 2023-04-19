import pygame

class Button:
    def __init__(self, x, y, scale, image_normal, image_hover):
        self.x = x
        self.y = y
        self.scale = scale
        self.image_normal = pygame.image.load(image_normal)
        self.image_hover = pygame.image.load(image_hover)
        self.surface = pygame.transform.scale_by(self.image_normal, self.scale)
        self.rect = self.surface.get_rect()
        self.rect.center = (self.x, self.y)

    def process(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.surface = pygame.transform.scale_by(self.image_hover, self.scale)
        else:
            self.surface = pygame.transform.scale_by(self.image_normal, self.scale)