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
        self.respawn_status = False
        self.lose_hp_timer = 0
        self.hp = 3
        self.respawn_time = 0
        self.alive = True


    def update(self, dt, keys):
        self.move(dt, keys)
        self.in_bounds()
        if self.respawn_status:
            self.lose_hp_animation(dt)
        else:
            self.lose_hp_timer = 0
            self.image = self.images[0]
        if not self.alive:
            self.kill()


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


    def lose_hp_animation(self, dt):
        self.lose_hp_timer += dt

        if self.lose_hp_timer > 0.3:
            self.image.set_alpha(0)
        if self.lose_hp_timer < 0.3:
            self.image = self.images[2]
        if self.lose_hp_timer < 0.15:
            self.image = self.images[1]

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

