import pygame.font
import pygame
from pygame.sprite import Group
from liam import Liam

class Scoreboard:

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.text_colour = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        self.prep_high_score ()
        self.prep_level()
        self.prep_lives()

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = "Current Score: " + str(int(rounded_score))
        self.score_image = self.font.render(score_str, True, self.text_colour, self.settings.bg_colour)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.lives.draw(self.screen)

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score: " + str(int(high_score))
        self.high_score_image = self.font.render(high_score_str, True, self.text_colour, self.settings.bg_colour)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        level_str = "Level " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_colour, self.settings.bg_colour)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_lives(self):
        self.lives = Group()
        for number in range(self.stats.lives_left):
            life = Liam(self.ai_game)
            life.image = pygame.image.load('images/liam.png')
            life.rect = life.image.get_rect()
            life.rect.x = number * life.rect.width
            life.rect.y = 10
            self.lives.add(life)