class Settings:
    """Stores all game settings"""

    def __init__(self):
        self.screen_width = 1920            #Sets window resolution
        self.screen_height = 1080
        self.bg_colour = (255, 255, 255)    #Sets background colour (R,G,B = 0-255)

        self.life_limit = 3                 #Sets max number of lives
        self.bullet_width, self.bullet_height = 3, 15
        self.bullet_colour = (255, 0 , 100)
        self.bullet_allowed = 3
        self.fleet_drop_speed = 50          #Sets target vertical drop
        self.speedup_scale = 1.1            #Sets target level scaling
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.liam_speed = 6                 #Sets character movement speed
        self.bullet_speed = 3               #Sets bullet travel speed
        self.target_speed = 1               #Sets target horizontal movement speed
        self.fleet_direction = 1
        self.target_points = 50

    def increase_speed(self):
        self.bullet_speed *= self.speedup_scale
        self.target_speed *= self.speedup_scale
        self.target_points *= self.score_scale