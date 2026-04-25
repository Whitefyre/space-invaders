import pygame
import random

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
        self.background_color = (10, 20, 40)

        self.white_stars_speed = 1
        self.warm_stars_speed = 1.5
        self.blue_stars_speed = 2

        self.player = Player(*PLAYER_POS)
        self.player_group = pygame.sprite.Group(self.player)
        self.player_bullet_group = pygame.sprite.Group()

        self.alien = Alien(ALIEN_POS_X, ALIEN_POS_Y, alien_type)
        self.alien_group = pygame.sprite.Group()
        self.alien_bullet_group = pygame.sprite.Group()

        self.clock = pygame.time.Clock()
        self.delta_time = self.clock.tick(144) / 1000.0
        self.running = True

        self.direction = 1


    def update(self):
        self.creating_stars()

        self.move_stars(self.white_stars_color, self.white_stars, self.white_stars_speed)
        self.move_stars(self.warm_stars_color, self.warm_stars, self.warm_stars_speed)
        self.move_stars(self.blue_stars_color, self.blue_stars, self.blue_stars_speed)

        self.handle_collision()

        self.create_aliens()
        self.alien_shooting()
        self.alien_hit_wall()

        self.event_types()

        self.handle()

    def draw(self, screen):
        screen.fill(self.background_color)





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


    def create_aliens(self):
        for row in range(ALIEN_ROW):
            for col in range(ALIEN_COL):
                ALIEN_POS_X = START_X_POSITION + col * HORIZONTAL_STEP
                ALIEN_POS_Y = START_Y_POSITION + row * VERTICAL_STEP
                if row == 0:
                    alien_type = 0
                elif row == 1:
                    alien_type = 1
                elif row == 2:
                    alien_type = 2
                elif row == 3:
                    alien_type = 3
                elif row == 4:
                    alien_type = 4

                alien = Alien(ALIEN_POS_X, ALIEN_POS_Y, alien_type)
                self.alien_group.add(alien)

    def alien_shooting(self):
        alien_list = list(self.alien_group.sprites())
        random_alien = alien_list[random.randint(0, len(alien_list) - 1)]
        x, y = random_alien.fire()
        if len(self.alien_bullet_group) < MAXIMUM_NUMBER_OF_ALIEN_BULLETS:
            bullet = Bullet(x, y, "alien")
            self.alien_bullet_group.add(bullet)


    def event_types(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                ###FIRE
                if event.key == pygame.K_SPACE:
                    x, y = self.player.fire()
                    if len(self.player_bullet_group) == 0:
                        bullet = Bullet(x, y, "player")
                        self.player_bullet_group.add(bullet)


    def alien_hit_wall(self):
        hit_wall = False
        for sprite in self.alien_group:
            if sprite.rect.right >= SCREEN_RIGHT or sprite.rect.left <= SCREEN_LEFT:
                hit_wall = True
                break
        if hit_wall:
            self.direction *= -1
            for alien in self.alien_group:
                alien.rect.centery += 10


    def handle(self):
        keys = pygame.key.get_pressed()
        self.player_group.update(self.delta_time, keys)
        self.player_group.draw(self.screen)
        self.player_bullet_group.update()
        self.player_bullet_group.draw(self.screen)
        self.alien_group.update(self.delta_time, self.direction)
        self.alien_group.draw(self.screen)
        self.alien_bullet_group.update()
        self.alien_bullet_group.draw(self.screen)
        pygame.display.flip()