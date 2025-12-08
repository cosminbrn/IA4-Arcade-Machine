import pygame
import os
from .observers import Observer
from .commands import *
from .resource_manager import ResourceManager
from .card_renderer import CardRenderer
from .animation_manager import AnimationManager

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

	def update(self, subject):
		# Delegate state tracking to manager
		self.anim_manager.update_state(self.model)
		self.draw()

	def draw_background_sliced(self, bg):
		# Slice logic to prevent stretching headers/middle excessively
		# Assuming header is top ~100px, footer is bottom ~100px
		img_w, img_h = bg.get_size()

		top_slice_h = 120
		bottom_slice_h = 120

		# Source Rects
		src_top = pygame.Rect(0, 0, img_w, top_slice_h)
		src_bottom = pygame.Rect(0, img_h - bottom_slice_h, img_w, bottom_slice_h)
		src_mid = pygame.Rect(0, top_slice_h, img_w, img_h - top_slice_h - bottom_slice_h)

		# Dest Rects (Virtual Screen)
		dest_top = pygame.Rect(0, 0, globals.VIRTUAL_WIDTH, top_slice_h)
		dest_bottom = pygame.Rect(0, globals.VIRTUAL_HEIGHT - bottom_slice_h, globals.VIRTUAL_WIDTH, bottom_slice_h)
		# Middle fills the rest
		dest_mid = pygame.Rect(0, top_slice_h, globals.VIRTUAL_WIDTH, globals.VIRTUAL_HEIGHT - top_slice_h - bottom_slice_h)

		# Draw Slices (Scale width, keep height for top/bottom, scale mid)
		# Note: transform.scale expects (width, height)

		# Top
		top_surf = bg.subsurface(src_top)
		self.screen.blit(pygame.transform.scale(top_surf, (dest_top.width, dest_top.height)), dest_top)

		# Bottom
		bottom_surf = bg.subsurface(src_bottom)
		self.screen.blit(pygame.transform.scale(bottom_surf, (dest_bottom.width, dest_bottom.height)), dest_bottom)

		# Mid
		mid_surf = bg.subsurface(src_mid)
		self.screen.blit(pygame.transform.scale(mid_surf, (dest_mid.width, dest_mid.height)), dest_mid)

	def draw(self):
		# Background - Metin2 Border
		bg = self.rm.load_image("ui/background.png")
		if bg:
			self.draw_background_sliced(bg)
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
