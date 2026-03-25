import pygame
screen = pygame.display.set_mode((800, 600))
import pytmx
import pyscroll
from pyscroll.group import PyscrollGroup
import random

tmx_data = pytmx.load_pygame("test_map.tmx")
map_layer = pyscroll.data.TiledMapData(tmx_data)
map_renderer = pyscroll.orthographic.BufferedRenderer(map_layer, screen.get_size())

group = PyscrollGroup(map_layer=map_renderer, default_layer=0)

def get_frame(sheet, x, y, w, h):
    frame = pygame.Surface((w, h), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), (x, y, w, h))
    return frame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 90, 1)
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)


    def update(self):
        self.rect.centery -= 5
        self.death()


    def death(self):
        if self.rect.bottom < 0:
            self.kill()



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_frame(SPRITE_SHEET, 68, 4, 9, 10)
        self.image = pygame.transform.scale_by(self.image, 10)
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.speed = 300


    def update(self, dt, keys):
        if keys[pygame.K_LEFT]:
            self.rect.centerx -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            self.rect.centerx += self.speed * dt
        if keys[pygame.K_z]:
            self.fire()


    def fire(self):
        if len(bullet_group) == 0:
            new_bullet = Bullet(self.rect.centerx, self.rect.centery - 30)
            bullet_group.add(new_bullet)


class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_frame(SPRITE_SHEET, 4, 20, 8, 7)
        self.image = pygame.transform.scale_by(self.image, 10)
        self.rect = self.image.get_frect()
        self.rect.center = (x, y)
        self.direction = True
        self.speed = 400

    def update(self, dt):
        self.movement(dt)


    def movement(self, dt):
        if self.direction:
            self.rect.centerx += self.speed * dt
            if self.rect.right > 800:
                self.direction = False
        else:
            self.rect.centerx -= self.speed * dt
            if self.rect.left < 0:
                self.direction = True


SPRITE_SHEET = pygame.image.load("Sprites/SpaceInvaders.png").convert_alpha()

player = Player(400,550)
player_group = pygame.sprite.Group(player)

bullet_group = pygame.sprite.Group()


alien = Alien(400,250)
alien_group = pygame.sprite.Group(alien)


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

# radius = random.choice([1, 1, 1, 10])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    delta_time = clock.tick(144) / 1000.0
    screen.fill(background_color)

    for x,y in blue_stars:
        pygame.draw.circle(screen, blue_color, (x, y), random.choice([1, 1, 1, 2]))

    for x,y in white_stars:
        pygame.draw.circle(screen, white_color, (x, y), random.choice([1, 1, 1, 2]))

    for x,y in warm_stars:
        pygame.draw.circle(screen, warm_color, (x, y), random.choice([1, 1, 1, 2]))

    keys = pygame.key.get_pressed()
    player_group.update(delta_time, keys)
    player_group.draw(screen)
    bullet_group.update()
    bullet_group.draw(screen)
    alien_group.update(delta_time)
    alien_group.draw(screen)
    pygame.display.flip()

pygame.quit()