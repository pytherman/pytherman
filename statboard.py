import pygame, pygame.font
from pygame.sprite import Sprite


class Statboard(Sprite):
    def __init__(self, screen):
        Sprite.__init__(self)
        self.screen = screen

        self.level = 0
        self.hp = 0
        self.points = 0

        self.sb_height = 40
        self.sb_width = self.screen.get_width()
        self.rect = pygame.Rect(0, 0, self.sb_width, self.sb_height)

        self.bg_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('Arial', 18)

        self.x_level_pos = 20
        self.y_level_pos = 10

        self.x_hp_pos = 120
        self.y_hp_pos = 10

        self.x_points_pos = 220
        self.y_points_pos = 10

    def prep_scores(self):
        self.level_string = "Level: " + str(self.level)
        self.level_image = self.font.render(self.level_string, True, self.text_color)
        self.hp_string = "Lives: " + str(self.hp)
        self.hp_image = self.font.render(self.hp_string, True, self.text_color)
        self.points_string = "Points: " + str(self.points)
        self.points_image = self.font.render(self.points_string, True, self.text_color)

    def blit(self):
        self.prep_scores()
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.level_image, (self.x_level_pos, self.y_level_pos))
        self.screen.blit(self.hp_image, (self.x_hp_pos, self.y_hp_pos))
        self.screen.blit(self.points_image, (self.x_points_pos, self.y_points_pos))
        # pygame.display.flip()
