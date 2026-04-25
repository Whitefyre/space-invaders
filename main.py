import pygame
from game import Game
pygame.init()
game = Game()
while game.running:
    game.update()
    game.draw()
pygame.quit()