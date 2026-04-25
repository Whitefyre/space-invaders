import pygame
import random

from pygame.sprite import groupcollide

from settings import *
from alien import Alien
from player import Player
from bullet import Bullet
from utils import get_frame


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def creating_stars(number):
    stars = []
    for _ in range(number):
        stars.append((random.randint(0, 800), random.randint(0, 600)))
    return stars


def moving_stars(color, stars, speed):
    for i in range(len(stars)):
        x, y = stars[i]
        y += speed
        pygame.draw.circle(screen, color, (x, y), 1)
        if y > SCREEN_BOTTOM:
            y = SCREEN_TOP
            x = random.randint(SCREEN_LEFT, SCREEN_RIGHT)
        stars[i] = (x, y)


player = Player(*PLAYER_POS)
player_group = pygame.sprite.Group(player)

player_bullet_group = pygame.sprite.Group()

alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()

direction = 1


def player_bullet_to_alien_collision():
    collisions = pygame.sprite.groupcollide(player_bullet_group, alien_group, True, False)
    for bullet, aliens in collisions.items():
        for alien in aliens:
            alien.death_switch()


def alien_bullet_to_player_collision():
    for bullet in alien_bullet_group:
        if bullet.rect.colliderect(player):
            bullet.kill()
            player.take_damage(bullet.damage)


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

        new_alien = Alien(ALIEN_POS_X, ALIEN_POS_Y, alien_type)
        alien_group.add(new_alien)


def alien_shooting():
    alien_list = list(alien_group.sprites())
    random_alien = alien_list[random.randint(0, len(alien_list) - 1)]
    x, y = random_alien.fire()
    if len(alien_bullet_group) < MAXIMUM_NUMBER_OF_ALIEN_BULLETS:
        bullet = Bullet(x, y, "alien")
        alien_bullet_group.add(bullet)



pygame.init()

clock = pygame.time.Clock()
running = True

background_color = (10, 20, 40)

number_of_white_stars = creating_stars(100)
number_of_warm_stars = creating_stars(100)
number_of_blue_stars = creating_stars(100)

while running:
    # GAME LOGIC

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ###FIRE
            if event.key == pygame.K_SPACE:
                x, y = player.fire()
                if len(player_bullet_group) == 0:
                    bullet = Bullet(x, y, "player")
                    player_bullet_group.add(bullet)
    delta_time = clock.tick(144) / 1000.0

    hit_wall = False
    for sprite in alien_group:
        if sprite.rect.right >= SCREEN_RIGHT or sprite.rect.left <= SCREEN_LEFT:
            hit_wall = True
            break
    if hit_wall:
        direction *= -1
        for alien in alien_group:
            alien.rect.centery += 10

    #GRAPHICS

    screen.fill(background_color)

    #STARS
    moving_stars((230, 230, 255), number_of_white_stars, 1)
    moving_stars((255, 240, 180), number_of_warm_stars, 1.5)
    moving_stars((180, 200, 255), number_of_blue_stars, 2)

    # if len(alien_group) > 0:
    #     alien_shooting()
    player_bullet_to_alien_collision()
    alien_bullet_to_player_collision()
    keys = pygame.key.get_pressed()
    player_group.update(delta_time, keys)
    player_group.draw(screen)
    player_bullet_group.update()
    player_bullet_group.draw(screen)
    alien_group.update(delta_time, direction)
    alien_group.draw(screen)
    alien_bullet_group.update()
    alien_bullet_group.draw(screen)
    pygame.display.flip()

pygame.quit()