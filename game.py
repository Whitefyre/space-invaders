import pygame
import random

from main import creating_stars
from settings import *
from alien import Alien
from player import Player
from bullet import Bullet
from utils import get_frame

class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.stars_number = 100

        self.white_stars = self.creating_stars()
        self.warm_stars = self.creating_stars()
        self.blue_stars = self.creating_stars()

        self.white_stars_color = (230, 230, 255)
        self.warm_stars_color = (255, 240, 180)
        self.blue_stars_color = (180, 200, 255)

        self.white_stars_speed = 1
        self.warm_stars_speed = 1.5
        self.blue_stars_speed = 2

        self.player = Player(*PLAYER_POS)
        self.player_group = pygame.sprite.Group(self.player)
        self.player_bullet_group = pygame.sprite.Group()

        self.alien_group = pygame.sprite.Group()
        self.alien_bullet_group = pygame.sprite.Group()

        self.direction = 1


    def update(self):
        self.creating_stars()

        self.move_stars(self.white_stars_color, self.white_stars, self.white_stars_speed)
        self.move_stars(self.warm_stars_color, self.warm_stars, self.warm_stars_speed)
        self.move_stars(self.blue_stars_color, self.blue_stars, self.blue_stars_speed)

        self.handle_collision()



    def creating_stars(self):
            stars = []
            for _ in range(self.stars_number):
                stars.append((random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))
            return stars


    def move_stars(self, color, stars, speed):
        for i in range(len(stars)):
            x, y = stars[i]
            y += speed
            pygame.draw.circle(self.screen, color, (x, y), 1)
            if y > SCREEN_BOTTOM:
                y = SCREEN_TOP
                x = random.randint(SCREEN_LEFT, SCREEN_RIGHT)
            stars[i] = (x, y)


    def handle_collision(self):
        collisions = pygame.sprite.groupcollide(self.player_bullet_group, self.alien_group, True, False)
        for bullet, aliens in collisions.items():
            for alien in aliens:
                alien.death_switch()
        for bullet in self.alien_bullet_group:
            if bullet.rect.colliderect(self.player):
                bullet.kill()
                self.player.take_damage(bullet.damage)
