import pygame
import os
from .observers import Observer
from .commands import *
from .resource_manager import ResourceManager
from .card_renderer import CardRenderer
from .animation_manager import AnimationManager
from .utilities import handle_leaderboard, draw_leaderboard

from .settings import globals

# Constants for Layout
SCREEN_WIDTH = globals.VIRTUAL_WIDTH
SCREEN_HEIGHT = globals.VIRTUAL_HEIGHT

# Colors
COLOR_BG = (25, 25, 25)
COLOR_TEXT = (255, 255, 255)
COLOR_GOLD = (255, 215, 0)

# Module that handles the construction of the GUI

class GameView(Observer):
	def __init__(self, model, screen):
		self.model = model
		self.real_screen = screen

		# Calculate scaling
		run_w, run_h = globals.WINWIDTH, globals.WINHEIGHT
		virt_w, virt_h = globals.VIRTUAL_WIDTH, globals.VIRTUAL_HEIGHT

		self.scale = min(run_w / virt_w, run_h / virt_h) * 0.95
		self.offset_x = (run_w - virt_w * self.scale) // 2
		self.offset_y = (run_h - virt_h * self.scale) // 2 

		# Virtual surface for drawing
		self.screen = pygame.Surface((virt_w, virt_h))

		self.rm = ResourceManager()
		self.renderer = CardRenderer(self.screen, self.rm)
		self.model.attach(self)

		# UI constants
		self.card_width = 114
		self.card_height = 148
		self.hand_y = 100    # Top of screen
		self.combo_y = 400   # Middle
		self.deck_y = 700    # Bottom Left
		self.deck_x = 50

		# Pre-calculate Rects for click detection
		self.hand_rects = []
		# Calculate stride with 10px spacing
		stride_x = self.card_width + 10

		# Calculate start_x to center 5 cards
		total_hand_width = (5 * stride_x) - 10
		start_x = (SCREEN_WIDTH - total_hand_width) // 2

		for i in range(5):
			self.hand_rects.append(pygame.Rect(start_x + i * stride_x, self.hand_y, self.card_width, self.card_height))

		self.combo_rects = []
		# Center 3 cards
		total_combo_width = (3 * stride_x) - 10
		start_x_combo = (SCREEN_WIDTH - total_combo_width) // 2

		for i in range(3):
			self.combo_rects.append(pygame.Rect(start_x_combo + i * stride_x, self.combo_y, self.card_width, self.card_height))

		self.deck_rect = pygame.Rect(self.deck_x, self.deck_y, self.card_width, self.card_height)

		# Restart Button 
		btn_w, btn_h = 100, 40
		btn_x = (globals.VIRTUAL_WIDTH - btn_w) // 2
		btn_y = 900 # Bottom area
		self.restart_btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

		# Animation Manager
		self.anim_manager = AnimationManager(self.deck_rect, self.hand_rects, self.combo_rects)
		
		self.leaderboard_calculated = False
		self.leaderboard = []

	def update(self, subject):
		# Delegate state tracking to manager
		self.anim_manager.update_state(self.model)
		self.draw()

	def draw_background_fitted(self, bg):
		self.screen.fill((0, 0, 0)) # Fill with black first
		
		img_w, img_h = bg.get_size()
		virt_w, virt_h = globals.VIRTUAL_WIDTH, globals.VIRTUAL_HEIGHT
		
		scale = min(virt_w / img_w, virt_h / img_h)
		new_w = int(img_w * scale)
		new_h = int(img_h * scale)
		
		scaled_bg = pygame.transform.scale(bg, (new_w, new_h))
		
		x = (virt_w - new_w) // 2
		y = (virt_h - new_h) // 2
		
		self.screen.blit(scaled_bg, (x, y))

	def draw(self):
		if self.model.game_over:
			if not self.leaderboard_calculated:
				self.leaderboard = handle_leaderboard(self.real_screen, self.model.score)
				self.leaderboard_calculated = True
			
			self.draw_game_over_screen()
			return
		else:
			self.leaderboard_calculated = False

		# Background - Metin2 Border
		bg = self.rm.load_image("ui/background.png")
		if bg:
			self.draw_background_fitted(bg)
		else:
			 # Fallback if image missing
			 self.screen.fill((30, 35, 45))

		# Draw Slots (Visual placeholders)
		for rect in self.hand_rects:
			self.renderer.draw_slot(rect, "Hand")

		for rect in self.combo_rects:
			 self.renderer.draw_slot(rect, "Combo")

		# Draw Deck with Stack Effect
		count = len(self.model.deck.cards)

		# Visualize using static image
		deck_img = self.rm.load_image("ui/deck.png")

		if deck_img:
			img_rect = deck_img.get_rect(center=self.deck_rect.center)
			self.screen.blit(deck_img, img_rect)
		elif not self.model.deck.is_empty():
			 # Fallback: Draw one card back if image fails and deck not empty for safety
			 self.renderer.draw_card_back(self.deck_rect)
		elif count == 0:
			pygame.draw.rect(self.screen, (30,30,30), self.deck_rect, 2)

		# Bottom UI Bar Layout
		base_y = self.deck_rect.bottom

		font = self.rm.load_font(20)

		x_label_surf = font.render("X", True, COLOR_TEXT)
		x_label_rect = x_label_surf.get_rect(bottom=base_y - 5, left=self.deck_rect.right + 15)
		self.screen.blit(x_label_surf, x_label_rect)

		# Count container
		count_val = f"{count}" # Just number
		count_box_w = 50
		count_box_h = 30
		count_box_rect = pygame.Rect(x_label_rect.right + 10, base_y - count_box_h, count_box_w, count_box_h)
		self.draw_ui_container(count_box_rect, count_val, label_color=COLOR_TEXT)

		# Score label
		score_label_surf = font.render("Score", True, COLOR_TEXT)
		score_label_rect = score_label_surf.get_rect(bottom=base_y - 5, left=count_box_rect.right + 20)
		self.screen.blit(score_label_surf, score_label_rect)

		# Score container
		score_val = f"{self.model.score}"
		score_box_w = 80
		score_box_h = 30
		score_box_rect = pygame.Rect(score_label_rect.right + 10, base_y - score_box_h, score_box_w, score_box_h)
		self.draw_ui_container(score_box_rect, score_val, label_color=COLOR_TEXT)


		# Draw cards in hand
		for i, card in enumerate(self.model.hand):
			if card:
				self.renderer.draw_card(card, self.hand_rects[i])
		
		# Draw "Restart" Button
		btn_rect = self.restart_btn_rect
		pygame.draw.rect(self.screen, (60, 60, 60), btn_rect, border_radius=5)   # Body
		pygame.draw.rect(self.screen, (120, 120, 120), btn_rect, 2, border_radius=5) # Highlight
		pygame.draw.rect(self.screen, (30, 30, 30), btn_rect.inflate(-2,-2), 1, border_radius=5) # Inner Shadow
		
		font_btn = self.rm.load_font(20)
		txt_surf = font_btn.render("Restart", True, COLOR_TEXT)
		txt_rect = txt_surf.get_rect(center=btn_rect.center)
		self.screen.blit(txt_surf, txt_rect)

		# Draw cards in combo
		for i, card in enumerate(self.model.combination):
			if card:
				self.renderer.draw_card(card, self.combo_rects[i])

		# Combo Points Indicator
		last_combo_rect = self.combo_rects[-1]
		combo_pts = self.model.current_combo_points

		pts_box_w = 60
		pts_box_h = 40
		pts_box_rect = pygame.Rect(last_combo_rect.right + 20, last_combo_rect.centery - pts_box_h//2, pts_box_w, pts_box_h)

		# High Score Effect (> 70)
		if combo_pts > 70:
			# Simple glow: Draw expanding/contracting border or bright color
			import time
			glow_val = (int(time.time() * 10) % 2) * 50 # 0 or 50
			color_glow = (255, 215 + glow_val/2, glow_val) # Gold to brighter
			pygame.draw.rect(self.screen, color_glow, pts_box_rect.inflate(6, 6), 3, border_radius=5)
		
		# Show points using "+ X" format
		pts_str = f"+ {combo_pts}" if combo_pts > 0 else "0"
		# Use smaller font if needed (logic inside draw_ui_container uses size 20, fits well)
		self.draw_ui_container(pts_box_rect, pts_str, label_color=COLOR_TEXT)



		# Draw Animations
		animations = self.anim_manager.update_animations()
		
		for anim in animations:
			rect = anim.update()
			self.renderer.draw_card(anim.card, rect)

		# Final blit to real screen
		scaled_w = int(globals.VIRTUAL_WIDTH * self.scale)
		scaled_h = int(globals.VIRTUAL_HEIGHT * self.scale)
		scaled_surface = pygame.transform.scale(self.screen, (scaled_w, scaled_h))

		self.real_screen.fill((6, 4, 4, 200)) # Black bars
		self.real_screen.blit(scaled_surface, (self.offset_x, self.offset_y))
		pygame.display.flip()

	def draw_game_over_screen(self):
		# Draw semi-transparent overlay
		s = pygame.Surface((globals.WINWIDTH, globals.WINHEIGHT), pygame.SRCALPHA)
		s.fill((0, 0, 0, 200))
		self.real_screen.blit(s, (0, 0))
		
		font = self.rm.load_font(72)
		text = font.render("Game Over", True, (255, 0, 0))
		text_rect = text.get_rect(center=(globals.WINWIDTH // 2, globals.WINHEIGHT // 2 - 150))
		self.real_screen.blit(text, text_rect)
		
		score_text = self.rm.load_font(48).render(f"Final Score: {self.model.score}", True, (255, 255, 255))
		score_rect = score_text.get_rect(center=(globals.WINWIDTH // 2, globals.WINHEIGHT // 2 - 70))
		self.real_screen.blit(score_text, score_rect)
		
		draw_leaderboard(self.real_screen, self.leaderboard, globals.WINHEIGHT // 2 + 50)
		
		tip_text = self.rm.load_font(48).render("Press ESC to return to menu", True, (200, 200, 0))
		tip_rect = tip_text.get_rect(center=(globals.WINWIDTH // 2, globals.WINHEIGHT - 50))
		self.real_screen.blit(tip_text, tip_rect)
		
		pygame.display.flip()

	def draw_ui_container(self, rect, text, label_color=(255, 255, 255)):
		s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
		s.fill((0, 0, 0, 200)) # Semi-transparent black
		self.screen.blit(s, rect.topleft)
		pygame.draw.rect(self.screen, (100, 100, 100), rect, 1) # Grey Border

		font = self.rm.load_font(20)
		text_surf = font.render(text, True, label_color)
		text_rect = text_surf.get_rect(center=rect.center)
		self.screen.blit(text_surf, text_rect)

	def handle_click(self, pos, button):
		"""
		Returns a Command object based on click
		Button: 1=Left, 3=Right
		"""
		# Transform pos from Screen Space to Virtual Space
		real_x, real_y = pos
		virt_x = (real_x - self.offset_x) / self.scale
		virt_y = (real_y - self.offset_y) / self.scale

		pos = (virt_x, virt_y)

		# Check Hand Clicks
		for i, rect in enumerate(self.hand_rects):
			if rect.collidepoint(pos):
				if button == 1: # Left Click -> Move to Combo
					return MoveToComboCommand(self.model, i)
				elif button == 3: # Right Click -> Discard
					return DiscardCardCommand(self.model, i)

		# Check Combo Clicks
		for i, rect in enumerate(self.combo_rects):
			if rect.collidepoint(pos):
				if button == 1: # Left Click -> Return to Hand
					return ReturnToHandCommand(self.model, i)

		# Check Deck Click
		if self.deck_rect.collidepoint(pos):
			if button == 1:
				return DrawCardCommand(self.model)

		# Check Restart
		if self.restart_btn_rect.collidepoint(pos):
			if button == 1:
				return ResetGameCommand(self.model)

		return None
