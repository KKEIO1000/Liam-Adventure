class GameStats:
    """Track statisitcs within the game"""

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        self.lives_left = self.settings.life_limit
        self.score = 0
        self.level = 1