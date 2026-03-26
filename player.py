import pygame
from utils import get_frame
from settings import SPRITE_SHEET

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_frame(SPRITE_SHEET, 68, 4, 9, 10)
        self.image = pygame.transform.scale_by(self.image, 10)
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.speed = 300


    def update(self, dt, keys):
        if keys[pygame.K_LEFT]:
            self.rect.centerx -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.rect.centerx += self.speed * dt


    def fire(self):
        return self.rect.centerx, self.rect.centery - 30