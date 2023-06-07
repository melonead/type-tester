import pygame

def load_image(path, color_key=(0, 0, 0)):
    img = pygame.image.load(path)
    img.set_colorkey(color_key)
    # img.convert()
    return img