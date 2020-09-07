import pygame
from pygame.sprite import Sprite

class Target(Sprite):
    """Class defines the shooting targerts"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/poo.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.rect.width, self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self):
        """Chekcs if fleet has hit the right edge"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <=0:
            return True

    def update(self):
        """Move targets to the right or left"""
        self.x += (self.settings.target_speed * self.settings.fleet_direction)
        self.rect.x = self.x

