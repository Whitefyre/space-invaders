import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (100,6))
        self.image = pygame.transform.rotozoom(self.image, 90, 1)
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)


    def update(self):
        self.rect.centery -= 5
        self.death()


    def death(self):
        if self.rect.bottom < 0:
            self.kill()