import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Bullet class fired by Liam"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen, self.settings = ai_game.screen, ai_game.settings
        self.colour = self.settings.bullet_colour
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.liam.rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        """Bullet travels up the screen"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.colour, self.rect)