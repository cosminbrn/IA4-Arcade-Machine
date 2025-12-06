import pygame
import math
from .utilities import *
from .constants import *

class Score:
    def __init__(self):
        self.value = 0
        font_path = "././assets/fonts/Pixellettersfull-BnJ5.ttf"
        self.font = pygame.font.Font(font_path, 36)
        self.combo_counter = 0
        self.missed_counter = 0

    def add_points(self, points):
        self.value += points

    def add_combo(self):
        if self.combo_counter > 10:
            self.value += COMBO_BASE_SCORE * (2 ** (self.combo_counter // 10))
        self.combo_counter = 0

    def add_missed(self):
        self.value -= MISSED_PENALTY * self.missed_counter
        self.missed_counter = 0

    def close_call(self):
        self.add_points(CLOSE_CALL_POINTS)

    def reset(self):
        self.value = 0

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.value}", True, (255, 255, 255))
        combo_text = self.font.render(f"Combo: {self.combo_counter}", True, (255, 255, 255))
        missed_text = self.font.render(f"Missed: {self.missed_counter}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(combo_text, (10, 50))
        screen.blit(missed_text, (10, 90))
