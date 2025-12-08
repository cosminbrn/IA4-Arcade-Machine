import random
import time
from collections import deque
from observers import Subject

class Card:
	def __init__(self, number, color):
		self.number = number # 1-8
		self.color = color   # 'red', 'yellow', 'blue'
	
	def __repr__(self):
		return f"{self.color}_{self.number}"

class Deck:
	def __init__(self):
		self.cards = [] 
		colors = ['red', 'blue', 'yellow']
		
		for number in range(1, 9):
			for color in colors:
				self.cards.append(Card(number, color))
		
	def shuffle(self):
		l = list(self.cards)
		random.shuffle(l)
		# Smart shuffle
		while self.check_shuffle() == False:
			random.shuffle(l)
		self.cards = deque(l)

	# Returns True when the deck is well shuffled
	def check_shuffle(self):
		if self.has_big_pair() or self.has_three_same_color():
			return False
		return True

	def has_big_pair(self):
		for curr_card, next_card in zip(self.cards, self.cards[1:]):
			if curr_card.number > 5 and \
			   curr_card.number == (next_card.number - 1) and \
			   curr_card.color == next_card.color:
				return True
		return False
		
	# Returns True if starting hand contains three cards of the same color
	def has_three_same_color(self):
		color_counts = {}
		for Card in self.cards[:5]:
			color_counts[Card.color] = color_counts.get(Card.color, 0) + 1
			if color_counts[Card.color] >= 3:
				return True
		return False

	def draw(self):
		if len(self.cards) > 0:
			return self.cards.popleft()
		return None
	
	def is_empty(self):
		return len(self.cards) == 0

class GameModel(Subject):
	def __init__(self):
		super().__init__()
		self.deck = Deck()
		self.deck.shuffle()
		
		# 5 cards in hand
		self.hand = [None] * 5 
		
		# 3 cards in combination
		self.combination = [None] * 3
		
		self.score = 0
		self.game_over = False
		self.message = ""

	@property
	def current_combo_points(self):
		if any(c is None for c in self.combination):
			return 0
		return self.calculate_points(*self.combination)

	def start_game(self):
		self.deck = Deck()
		self.deck.shuffle()
		self.hand = [None] * 5
		self.combination = [None] * 3
		self.score = 0
		self.game_over = False
		self.notify()

	def fill_hand_initial(self):
		for i in range(5):
			if self.hand[i] is None:
				card = self.deck.draw()
				if card:
					self.hand[i] = card

	def draw_card_action(self):
		if all(card is None for card in self.hand):
			 self.fill_hand_initial()
			 self.notify()
			 return

		# Draw 1 card into first empty slot
		slot_index = -1
		for i in range(5):
			if self.hand[i] is None:
				slot_index = i
				break
		
		if slot_index != -1:
			card = self.deck.draw()
			if card:
				self.hand[slot_index] = card
				self.notify()
			else:
				self.check_game_over()

	def discard_card(self, hand_index):
		if 0 <= hand_index < 5:
			if self.hand[hand_index] is not None:
				self.hand[hand_index] = None
				self.notify()
				self.check_game_over()

	def move_hand_to_combo(self, hand_index):
		if 0 <= hand_index < 5 and self.hand[hand_index] is not None:
			# Find empty combo slot
			combo_index = -1
			for i in range(3):
				if self.combination[i] is None:
					combo_index = i
					break
			
			if combo_index != -1:
				self.combination[combo_index] = self.hand[hand_index]
				self.hand[hand_index] = None
				
				self.notify()
				
				self.check_combination_match() 

	def return_combo_to_hand(self, combo_index):
		if 0 <= combo_index < 3 and self.combination[combo_index] is not None:
			# Find empty hand slot
			hand_index = -1
			for i in range(5):
				if self.hand[i] is None:
					hand_index = i
					break
			
			if hand_index != -1:
				self.hand[hand_index] = self.combination[combo_index]
				self.combination[combo_index] = None
				self.notify()

	def check_combination_match(self):
		# Check if 3 cards are present
		if any(c is None for c in self.combination):
			return

		c1, c2, c3 = self.combination
		points = self.calculate_points(c1, c2, c3)
		
		if points > 0:
			time.sleep(0.6)
			
			self.score += points
			self.message = f"Success! +{points}"
			self.combination = [None, None, None]
			self.notify()
		else:
			self.message = "Invalid Combination"
			self.notify()

	def calculate_points(self, c1, c2, c3):
		cards = sorted([c1, c2, c3], key=lambda x: x.number)
		x, y, z = cards[0].number, cards[1].number, cards[2].number
		
		same_col = (c1.color == c2.color == c3.color)
		
		# 1. Same Number (Set)
		if x == y == z:
			return (x + 1) * 10 
					
		# 2. Consecutive (Run)
		if x + 1 == y and y + 1 == z:
			# Color matters for runs
			if same_col:
				if (x, y, z) == (6, 7, 8): return 100
				if (x, y, z) == (5, 6, 7): return 90
				if (x, y, z) == (4, 5, 6): return 80
				if (x, y, z) == (3, 4, 5): return 70
				if (x, y, z) == (2, 3, 4): return 60
				if (x, y, z) == (1, 2, 3): return 50
			else:
				if (x, y, z) == (6, 7, 8): return 50
				if (x, y, z) == (5, 6, 7): return 50
				if (x, y, z) == (4, 5, 6): return 40
				if (x, y, z) == (3, 4, 5): return 30
				if (x, y, z) == (2, 3, 4): return 20
				if (x, y, z) == (1, 2, 3): return 10

		return 0

	def check_game_over(self):
		if self.deck.is_empty() and all(c is None for c in self.hand) and all(c is None for c in self.combination):
			self.game_over = True
