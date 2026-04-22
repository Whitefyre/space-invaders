import pygame
from utils import get_frame
from settings import SPRITE_SHEET

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_frame(SPRITE_SHEET, 39, 5, 1, 6)
        self.image = pygame.transform.scale(self.image, (3, 20))
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)


    def update(self):
        self.rect.centery -= 5
        self.death()


    def death(self):
        if self.rect.bottom < 0:
            self.kill()