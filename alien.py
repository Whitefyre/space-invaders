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
        self.direction = 1
        self.speed = 70
        self.move_timer = 0
        self.walking_permission = False

    def update(self, dt):
        self.new_movement(dt)

    def new_movement(self, dt):
        self.move_timer += dt

        if self.move_timer < 0.3:
            self.rect.centerx += self.speed * dt * self.direction

        if self.move_timer >= 0.6:
            self.move_timer = 0

        if self.rect.right > 800 or self.rect.left < 0:
            self.direction *= -1
    # def movement(self, dt):
    #     if self.direction:
    #         self.rect.centerx += self.speed * dt
    #         if self.rect.right > 800:
    #             self.direction = False
    #     else:
    #         self.rect.centerx -= self.speed * dt
    #         if self.rect.left < 0:
    #             self.direction = True