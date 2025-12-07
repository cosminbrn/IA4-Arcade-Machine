import pygame
from constants import *

class HandGame:
	def __init__(self, image, side, screen_width, screen_height):
		self.side = side
		self.image = image
		self.screen_width = screen_width
		self.screen_height = screen_height
		
		self.speed = HAND_START_SPEED
		
		self.reset()
		self.passed_present = False
		self.active = True
		self.last_reset_time = 0
		self.delay_after_reset = HAND_RESPAWN_DELAY

	def reset(self):
		self.y = - self.image.get_height()
		if self.side == "left":
			self.x = 0
		else:
			self.x = self.screen_width - self.image.get_width()
		self.passed_present = False
		self.active = False
		self.last_reset_time = pygame.time.get_ticks()

	def update(self):
		current_time = pygame.time.get_ticks()
		if not self.active:
			if current_time - self.last_reset_time >= self.delay_after_reset:
				self.active = True
			else:
				return
		
		if self.speed < HAND_MAX_SPEED:
			self.speed += HAND_ACCEL

		self.y += self.speed
		if self.y > self.screen_height:
			self.reset()

	def draw(self, screen):
		if self.active:
			screen.blit(self.image, (self.x, self.y))
