import pygame
import random

from settings import *
from alien import Alien
from player import Player
from bullet import Bullet


class Game:
    def __init__(self):
        # Main window used by the whole game.
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Timing and loop state.
        self.clock = pygame.time.Clock()
        self.running = True
        self.direction = 1

        # Background style.
        self.background_color = (10, 20, 40)
        self.white_stars = self.creating_stars(100)
        self.warm_stars = self.creating_stars(100)
        self.blue_stars = self.creating_stars(100)

        # Player and sprite groups.
        self.player = Player(*PLAYER_POS)
        self.player_group = pygame.sprite.Group(self.player)
        self.player_bullet_group = pygame.sprite.Group()
        self.alien_group = pygame.sprite.Group()
        self.alien_bullet_group = pygame.sprite.Group()

        # Create the starting alien formation once.
        self.create_aliens()

    def creating_stars(self, number):
        # Create random star positions for the parallax background.
        stars = []
        for _ in range(number):
            stars.append((random.randint(0, 800), random.randint(0, 600)))
        return stars

    def moving_stars(self, color, stars, speed):
        # Move stars downward and recycle them at the top when needed.
        for i in range(len(stars)):
            x, y = stars[i]
            y += speed
            pygame.draw.circle(self.screen, color, (x, y), 1)
            if y > SCREEN_BOTTOM:
                y = SCREEN_TOP
                x = random.randint(SCREEN_LEFT, SCREEN_RIGHT)
            stars[i] = (x, y)

    def player_bullet_to_alien_collision(self):
        # Player bullets mark aliens for death and are removed on hit.
        collisions = pygame.sprite.groupcollide(self.player_bullet_group, self.alien_group, True, False)
        for bullet, aliens in collisions.items():
            for alien in aliens:
                alien.death_switch()

    def alien_bullet_to_player_collision(self):
        # Alien bullets damage the player and disappear on hit.
        for bullet in self.alien_bullet_group:
            if bullet.rect.colliderect(self.player):
                bullet.kill()
                self.player.take_damage(bullet.damage)

    def create_aliens(self):
        # Build a 5-row formation with types based on row index.
        for row in range(ALIEN_ROW):
            for col in range(ALIEN_COL):
                alien_pos_x = START_X_POSITION + col * HORIZONTAL_STEP
                alien_pos_y = START_Y_POSITION + row * VERTICAL_STEP
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

                new_alien = Alien(alien_pos_x, alien_pos_y, alien_type)
                self.alien_group.add(new_alien)

    def alien_shooting(self):
        # Pick a random alien shooter and spawn a bullet if limit allows.
        alien_list = list(self.alien_group.sprites())
        random_alien = alien_list[random.randint(0, len(alien_list) - 1)]
        x, y = random_alien.fire()
        if len(self.alien_bullet_group) < MAXIMUM_NUMBER_OF_ALIEN_BULLETS:
            bullet = Bullet(x, y, "alien")
            self.alien_bullet_group.add(bullet)

    def handle_events(self):
        # Handle quit and firing input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    x, y = self.player.fire()
                    if len(self.player_bullet_group) == 0:
                        bullet = Bullet(x, y, "player")
                        self.player_bullet_group.add(bullet)

    def alien_hit_wall(self):
        # Reverse movement direction if any alien touches side bounds.
        hit_wall = False
        for sprite in self.alien_group:
            if sprite.rect.right >= SCREEN_RIGHT or sprite.rect.left <= SCREEN_LEFT:
                hit_wall = True
                break
        if hit_wall:
            self.direction *= -1
            for alien in self.alien_group:
                alien.rect.centery += 10

    def update(self):
        # Update gameplay state once per frame.
        self.handle_events()
        delta_time = self.clock.tick(144) / 1000.0
        self.alien_hit_wall()
        self.player_bullet_to_alien_collision()
        self.alien_bullet_to_player_collision()
        keys = pygame.key.get_pressed()
        self.player_group.update(delta_time, keys)
        self.player_bullet_group.update()
        self.alien_group.update(delta_time, self.direction)
        self.alien_bullet_group.update()

        # Keep this disabled to preserve your current game behavior.
        if len(self.alien_group) > 0:
            self.alien_shooting()

    def draw(self):
        # Draw everything for the current frame.
        self.screen.fill(self.background_color)
        self.moving_stars((230, 230, 255), self.white_stars, 1)
        self.moving_stars((255, 240, 180), self.warm_stars, 1.5)
        self.moving_stars((180, 200, 255), self.blue_stars, 2)
        self.player_group.draw(self.screen)
        self.player_bullet_group.draw(self.screen)
        self.alien_group.draw(self.screen)
        self.alien_bullet_group.draw(self.screen)
        pygame.display.flip()