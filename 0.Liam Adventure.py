import sys
import pygame
from time import sleep
from setting import Settings
from liam import Liam
from bullet import Bullet
from target import Target
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Manages assets and behavior"""

    def __init__(self):
        """Game initialization"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Liam Survival")
        self.liam = Liam(self)
        self.stats = GameStats(self)
        self.bullets = pygame.sprite.Group()
        self.targets = pygame.sprite.Group()
        self._create_fleet()
        self.sb = Scoreboard(self)
        self.play_button = Button(self, 'play')

    def run_game(self):
        """Starts the game loop"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.liam.update()
                self._update_bullets()
                self._update_targets()
            self._update_screen()


    def _create_fleet(self):
        target = Target(self)
        target_width, target_height = target.rect.size
        available_space_x = self.settings.screen_width - (2*target_width)
        num_targets_x = available_space_x // (2 * target_width)

        available_space_y = (self.settings.screen_height - (3 * target_height) - self.liam.rect.height)
        number_rows = available_space_y // (2 * target_height)

        for row_number in range(number_rows):
            for num in range(num_targets_x):
                self._create_target(num, row_number)

    def _create_target(self, num, row_number):
        target = Target(self)
        target_width, target_height = target.rect.size
        target.x = target_width+2 * target_width * num
        target.rect.x = target.x
        target.rect.y = target.rect.height + 2 * target.rect.height * row_number
        self.targets.add(target)

    def _check_fleet_edges(self):
        """If fleet hit the end of the screen, change direction"""
        for target in self.targets.sprites():
            if target.check_edges():
                self._check_fleet_direction()
                break

    def _check_fleet_direction(self):
        """Reverses direction and drop down"""
        for target in self.targets.sprites():
            target.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _check_events(self):
        """Responds to keypress and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Starts new game after clicking play"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_lives()
            self.targets.empty()
            self.bullets.empty()
            self._create_fleet()
            self.liam.center()
            pygame.mouse.set_visible(False) #Hides mouse cursor


    def _check_keydown_events(self, event):
        """Responds to key press events"""
        if event.key == pygame.K_RIGHT:
            self.liam.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.liam.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Responds to key release events"""
        if event.key == pygame.K_RIGHT:
            self.liam.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.liam.moving_left = False

    def _check_bullet_target_collisions(self):
        """Responds to collisions"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.targets, True, True)
        if collisions:
            for targets in collisions.values():
                self.stats.score += self.settings.target_points
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.targets:            #Destroy exisiting bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _check_targets_bottom(self):
        screen_rect = self.screen.get_rect()
        for target in self.targets.sprites():
            if target.rect.bottom >= screen_rect.bottom:
                self._liam_hit()
                break

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _liam_hit(self):
        if self.stats.lives_left > 0:
            self.stats.lives_left -= 1
            self.targets.empty()
            self.bullets.empty()
            self._create_fleet()
            self.liam.center()
            self.sb.prep_lives()
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
        self._check_bullet_target_collisions()

    def _update_targets(self):
        self._check_fleet_edges()
        self.targets.update()
        if pygame.sprite.spritecollideany(self.liam, self.targets):
            self._liam_hit()
        self._check_targets_bottom()


    def _update_screen(self):
        """updates images on the screen and draws new screen"""
        self.screen.fill(self.settings.bg_colour)        #Redraw screen during each pass
        self.liam.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.targets.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip() #Make the newest drawn screen visible

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()