import pygame
import random
from alien import Alien
from player import Player
from bullet import Bullet
from utils import get_frame
from settings import SPRITE_SHEET

screen = pygame.display.set_mode((800, 600))

def one_line_down(group):
    for sprite in group:
        if sprite.rect.right > 800 or sprite.rect.left < 0:
            return True
    return False

player = Player(400,550)
player_group = pygame.sprite.Group(player)

bullet_group = pygame.sprite.Group()

x, y = 100, 250
alien_group = pygame.sprite.Group()
for alien in range(6):
    x += 50
    new_alien = Alien(x, y)
    alien_group.add(new_alien)




pygame.init()

clock = pygame.time.Clock()
running = True


white_stars = [(random.randint(0, 800), random.randint(0, 600)) for _ in range(100)]
warm_stars = [(random.randint(0, 800), random.randint(0, 600)) for _ in range(100)]
blue_stars = [(random.randint(0, 800), random.randint(0, 600)) for _ in range(100)]

white_color = (230, 230, 255)
warm_color = (255, 240, 180)
blue_color = (180, 200, 255)

background_color = (10, 20, 40)

while running:
    # GAME LOGIC

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ###FIRE
            if event.key == pygame.K_SPACE:
                x, y = player.fire()
                if len(bullet_group) == 0:
                    bullet = Bullet(x, y)
                    bullet_group.add(bullet)
    delta_time = clock.tick(144) / 1000.0

    #GRAPHICS

    screen.fill(background_color)

    for x,y in blue_stars:
        pygame.draw.circle(screen, blue_color, (x, y), random.choice([1, 1, 1, 2]))

    for x,y in white_stars:
        pygame.draw.circle(screen, white_color, (x, y), random.choice([1, 1, 1, 2]))

    for x,y in warm_stars:
        pygame.draw.circle(screen, warm_color, (x, y), random.choice([1, 1, 1, 2]))

    collisions = pygame.sprite.groupcollide(alien_group, bullet_group, True, True)

    if one_line_down(alien_group):
        for alien in alien_group:
            alien.direction *= -1
            alien.rect.centery += 10

    keys = pygame.key.get_pressed()
    player_group.update(delta_time, keys)
    player_group.draw(screen)
    bullet_group.update()
    bullet_group.draw(screen)
    alien_group.update(delta_time)
    alien_group.draw(screen)
    pygame.display.flip()

pygame.quit()