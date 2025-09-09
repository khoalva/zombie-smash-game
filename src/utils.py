import pygame
import os
import config

def load_image(filename, convert_alpha=True):
    """Load image with optional alpha channel support"""
    path = os.path.join(config.IMG_DIR, filename)
    if convert_alpha:
        return pygame.image.load(path).convert_alpha()
    else:
        return pygame.image.load(path).convert()

def get_random_position():
    """Get random position for zombie spawn, avoiding UI areas"""
    import random
    x = random.randint(60, config.SCREEN_WIDTH - 60)
    y = random.randint(120, config.SCREEN_HEIGHT - 60)
    return x, y
