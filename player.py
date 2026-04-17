import pygame
from utils import get_frame
from settings import SPRITE_SHEET

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_frame(SPRITE_SHEET, 68, 4, 9, 10)
        self.image = pygame.transform.scale(self.image, (32,32))
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.speed = 300


    def update(self, dt, keys):
        self.move(dt, keys)
        self.in_bounds()

    def move(self, dt, keys):
        if keys[pygame.K_LEFT]:
            self.rect.centerx -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.rect.centerx += self.speed * dt


    def in_bounds(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 800:
            self.rect.right = 800


    def fire(self):
        return self.rect.centerx, self.rect.centery - 30