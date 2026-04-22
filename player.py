import pygame
from utils import get_frame
from settings import SPRITE_SHEET

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            get_frame(SPRITE_SHEET, 68, 4, 9, 10),
            get_frame(SPRITE_SHEET, 34, 52, 13, 9),  # спрайт взрыва
            get_frame(SPRITE_SHEET, 33, 67, 15, 11)
        ]
        self.images = [pygame.transform.scale(img, (32, 32)) for img in self.images]
        self.image = self.images[0]
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.speed = 300
        self.death_status = False
        self.death_timer = 0
        self.hp = 3


    def update(self, dt, keys):
        self.move(dt, keys)
        self.in_bounds()
        if self.death_status:
            self.death(dt)

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


    def death(self, dt):
        self.death_timer += dt

        if self.death_timer > 0.3:
            self.kill()
        if self.death_timer < 0.3:
            self.image = self.images[2]
        if self.death_timer < 0.15:
            self.image = self.images[1]
