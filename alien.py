import pygame
from utils import get_frame
from settings import SPRITE_SHEET

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, alien_type):
        pygame.sprite.Sprite.__init__(self)
        self.images = {
        0: [
            get_frame(SPRITE_SHEET, 4, 20, 8, 8),#первый пришелец
            get_frame(SPRITE_SHEET, 20, 20, 8, 8),
        ],
        1: [
            get_frame(SPRITE_SHEET, 3, 4, 11, 8),#второй пришелец
            get_frame(SPRITE_SHEET, 19, 4, 11, 9),
        ],
        2: [
            get_frame(SPRITE_SHEET,4,36,9,8),
            get_frame(SPRITE_SHEET,19,36,11,8),
        ],
        3: [
            get_frame(SPRITE_SHEET,4,52,8,8),
            get_frame(SPRITE_SHEET,20,52,8,8),
        ],
        4: [
            get_frame(SPRITE_SHEET,4,68,8,8),
            get_frame(SPRITE_SHEET,20,68,8,8),
        ],
        5:[
            get_frame(SPRITE_SHEET, 34, 52, 13, 9),#спрайт взрыва
            get_frame(SPRITE_SHEET, 33, 67, 15, 11)
        ]
        }
        for key in self.images:
            self.images[key] = [pygame.transform.scale(img, (40, 32)) for img in self.images[key]]
        self.alien_type = alien_type
        self.frames = self.images[self.alien_type]
        self.frame = 0
        self.explosion_frames = self.images[5]
        self.image = self.frames[self.frame]
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.speed = 70
        self.move_timer = 0
        self.death_status = False
        self.death_timer = 0


    def update(self, dt, direction):
        self.new_movement(dt, direction)
        if self.death_status:
            self.death(dt)
        self.fire()


    def new_movement(self, dt, direction):
        self.move_timer += dt

        if self.move_timer < 0.3:
            self.rect.centerx += self.speed * dt * direction


        if self.move_timer >= 1:
            self.frame = (self.frame + 1) % len(self.frames)
            self.image = self.frames[self.frame]
            self.move_timer = 0


    def death(self, dt):
        self.death_timer += dt

        if self.death_timer > 0.6:
            self.kill()
        if self.death_timer < 0.6:
            self.image = self.explosion_frames[1]
        if self.death_timer < 0.3:
            self.image = self.explosion_frames[0]



    def fire(self):
        return self.rect.centerx, self.rect.centery + 10