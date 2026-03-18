# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
player_posx = 500
player_posy = 300
player_speed = 500

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    dt = clock.tick(60) / 1000.0
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("pink")
    pygame.draw.rect(screen, "black", (player_posx,player_posy, 50, 50))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_posy -= player_speed * dt
    if keys[pygame.K_DOWN]:
        player_posy += player_speed * dt
    if keys[pygame.K_LEFT]:
        player_posx -= player_speed * dt
    if keys[pygame.K_RIGHT]:
        player_posx += player_speed * dt
    # RENDER YOUR GAME HERE
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()