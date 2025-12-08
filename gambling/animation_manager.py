import pygame

class Animation:
	def __init__(self, card, start_rect, end_rect, duration=30):
		self.card = card
		self.start_rect = start_rect
		self.end_rect = end_rect
		self.duration = duration
		self.current_frame = 0
		self.finished = False
		
	def update(self):
		self.current_frame += 1
		if self.current_frame >= self.duration:
			self.finished = True
			return self.end_rect
			
		t = self.current_frame / self.duration
		# Ease-out cubic for smoother feel
		t = 1 - (1 - t)**3
		
		x = self.start_rect.x + (self.end_rect.x - self.start_rect.x) * t
		y = self.start_rect.y + (self.end_rect.y - self.start_rect.y) * t
		w = self.start_rect.width + (self.end_rect.width - self.start_rect.width) * t
		h = self.start_rect.height + (self.end_rect.height - self.start_rect.height) * t
		
		return pygame.Rect(int(x), int(y), int(w), int(h))

class AnimationManager:
	def __init__(self, deck_rect, hand_rects, combo_rects):
		self.deck_rect = deck_rect
		self.hand_rects = hand_rects
		self.combo_rects = combo_rects
		
		self.animations = []
		
		self.last_hand = [None] * 5
		self.last_combo = [None] * 3

	def update_state(self, model):
		# 1. Check Hand changes (Draw OR Return from Combo)
		for i in range(5):
			if model.hand[i] is not None and self.last_hand[i] is None:
				# Card appeared in hand[i]
				card = model.hand[i]
				start_rect = self.deck_rect # Default to Draw
				
				# Check if it came from Combo
				found_in_combo = False
				for c_idx, c_card in enumerate(self.last_combo):
					if c_card and c_card.number == card.number and c_card.color == card.color:
						start_rect = self.combo_rects[c_idx]
						found_in_combo = True
						break
				
				# Create animation
				anim = Animation(card, start_rect, self.hand_rects[i])
				self.animations.append(anim)
				
		# 2. Check Combo changes (Move from Hand)
		for i in range(3):
			if model.combination[i] is not None and self.last_combo[i] is None:
				# Card appeared in combo[i]
				card = model.combination[i]
				start_rect = self.deck_rect # Fallback
				
				# Check if it came from Hand
				found_in_hand = False
				for h_idx, h_card in enumerate(self.last_hand):
					if h_card and h_card.number == card.number and h_card.color == card.color:
						start_rect = self.hand_rects[h_idx]
						found_in_hand = True
						break
				
				if found_in_hand:
					anim = Animation(card, start_rect, self.combo_rects[i])
					self.animations.append(anim)
					
		# Update State
		self.last_hand = [c for c in model.hand] # Shallow copy
		self.last_combo = [c for c in model.combination]

	def update_animations(self):
		# Remove finished
		self.animations = [a for a in self.animations if not a.finished]
		return self.animations
