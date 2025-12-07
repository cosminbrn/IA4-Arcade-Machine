import pygame
from constants import WHITE, BLACK

class ScoreBoard:
	def __init__(self, x, y, w, h, font):
		self.rect = pygame.Rect(x, y, w, h)
		self.score = 0
		self.font = font

	def add_score(self):
		self.score += 1

	def draw(self, screen):
		pygame.draw.rect(screen, WHITE, self.rect)
		pygame.draw.rect(screen, BLACK, self.rect, 4)
		score_text = self.font.render(f"Score: {self.score}", True, BLACK)
		text_rect = score_text.get_rect(center=self.rect.center)
		screen.blit(score_text, text_rect)