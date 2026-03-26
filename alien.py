import pygame
from utils import get_frame
from settings import SPRITE_SHEET

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_frame(SPRITE_SHEET, 4, 20, 8, 7)
        self.image = pygame.transform.scale_by(self.image, 5)
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.direction = True
        self.speed = 150

    def update(self, dt):
        self.movement(dt)


    def movement(self, dt):
        if self.direction:
            self.rect.centerx += self.speed * dt
            if self.rect.right > 800:
                self.direction = False
        else:
            self.rect.centerx -= self.speed * dt
            if self.rect.left < 0:
                self.direction = True

alien = Alien(400,250)
alien_group = pygame.sprite.Group(alien)