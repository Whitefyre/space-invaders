import pygame

def get_frame(sheet, x, y, w, h):
    frame = pygame.Surface((w, h), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), (x, y, w, h))
    return frame