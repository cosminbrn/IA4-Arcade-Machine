import pygame
import random
from constants import *

class Flake:
	def __init__(self, screen_width, screen_height):
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.reset()
	
	def reset(self):
		self.x = random.randint(0, self.screen_width)
		self.y = random.randint(-self.screen_height, 0)
		self.speed = random.uniform(1, 3) * SCALE
		self.size = int(random.randint(4, 5) * (SCALE * 0.8))

	def update(self):
		self.y += self.speed
		self.x += random.uniform(-0.3, 0.3) * SCALE
		if self.y > self.screen_height:
			self.reset()
	
	def draw(self, screen):
		pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)