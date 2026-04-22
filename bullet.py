import pygame
from utils import get_frame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, owner):
        pygame.sprite.Sprite.__init__(self)
        self.images =[
            get_frame(SPRITE_SHEET, 39, 5, 1, 6),
            get_frame(SPRITE_SHEET, 38, 21, 3, 7)
        ]
        if owner == "player":
            self.images = [pygame.transform.scale (img, (5,20)) for img in self.images]
        if owner == "alien":
            self.images = [pygame.transform.scale(img, (15, 15)) for img in self.images]
        self.image = self.images[0]
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.owner = owner


    def update(self):
        if self.owner == "player":
            self.rect.centery -= 5
            self.death()
        elif self.owner == "alien":
            self.image = self.images[1]
            self.rect.centery += 3
            self.death()


    def death(self):
        if self.rect.bottom < 0:
            self.kill()
        elif self.rect.top > SCREEN_BOTTOM:
            self.kill()