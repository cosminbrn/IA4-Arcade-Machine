import pygame

# Colors for card rendering
COLOR_SLOT = (40, 40, 40)
COLOR_SLOT_BORDER = (100, 100, 100)
COLOR_RED = (200, 50, 50)
COLOR_BLUE = (50, 100, 200)
COLOR_YELLOW = (200, 200, 50)

class CardRenderer:
	def __init__(self, screen, resource_manager):
		self.screen = screen
		self.rm = resource_manager

	def draw_slot(self, rect, type_name):
		# Try to load placeholder image
		placeholder_img = self.rm.load_image("ui/placeholder_scaled.png", (rect.width, rect.height))

		if placeholder_img:
			self.screen.blit(placeholder_img, rect)
		else:
			# Fallback if image not found
			s = pygame.Surface((rect.width, rect.height))
			s.set_alpha(50)
			s.fill((0,0,0))
			self.screen.blit(s, rect.topleft)
			pygame.draw.rect(self.screen, (60, 60, 70), rect, 2)

	def draw_card(self, card, rect):
		# Try to load specific card asset
		# Expected naming: "cards/1_red.png", "cards/5_blue.png"
		image_key = f"cards/{card.number}_{card.color}.png"
		card_img = self.rm.load_image(image_key, (rect.width, rect.height))

		if card_img:
			self.screen.blit(card_img, rect)
			return

		# Fallback: Code Rendering
		pygame.draw.rect(self.screen, (240, 240, 240), rect)
		pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)

		# Color Stripe / Fill
		c = (100, 100, 100)
		if card.color == 'red': c = COLOR_RED
		elif card.color == 'blue': c = COLOR_BLUE
		elif card.color == 'yellow': c = COLOR_YELLOW

		inner_rect = rect.inflate(-10, -10)
		pygame.draw.rect(self.screen, c, inner_rect)

		# Number
		font = self.rm.load_font(60)
		text = font.render(str(card.number), True, (255, 255, 255))
		# Add simpler shadow/outline for contrast
		text_shadow = font.render(str(card.number), True, (0,0,0))

		text_rect = text.get_rect(center=rect.center)
		shadow_rect = text_rect.move(2, 2)

		self.screen.blit(text_shadow, shadow_rect)
		self.screen.blit(text, text_rect)

	def draw_card_back(self, rect):
		# Draw decorative back
		# Rounded corners for better look
		pygame.draw.rect(self.screen, (40, 120, 60), rect, border_radius=4)
		pygame.draw.rect(self.screen, (220, 220, 220), rect, 2, border_radius=4) 

		# Simple Patterns
		cx, cy = rect.centerx, rect.centery
		pygame.draw.circle(self.screen, (60, 140, 80), (cx, cy), 15)
