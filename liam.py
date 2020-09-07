import pygame
from pygame.sprite import Sprite

class Liam(Sprite):
    """A class to manage Liam."""

    def __init__(self, ai_game):
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/liam_original.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        self.moving_right, self.moving_left= False, False #Initialize Flags for movement

    def update(self):
        """Update Liam's position"""
        if self.moving_right and self.rect.left < self.screen_rect.right - self.rect.width:
            self.x += self.settings.liam_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.liam_speed
        self.rect.x = self.x

    def blitme(self):
        """Draw at current location."""
        self.screen.blit(self.image, self.rect)

    def center(self):
        """Reset at the center"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)