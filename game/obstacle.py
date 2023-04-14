import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, img_path):
        super().__init__()
        self.image = pygame.transform.scale_by(pygame.image.load(img_path), 0.125)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (pos_x, pos_y)

    def draw_rect(self):
        pass

    def update(self, decrement):
        self.rect.centerx -= decrement