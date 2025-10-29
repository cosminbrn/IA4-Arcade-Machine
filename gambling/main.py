import os
# os.environ.setdefault("PYGAME_DETECT_AVX2", "1")
import sys
import pygame
import random
from collections import deque

screen_width = 720
screen_height = 960

class GameState:
	def __init__(self):
		self.start = False
		self.end = False
		self.total_points = 0
		self.hand = [None] * 5
  
	# Initializes the deck and draws the hand
	def start_game(self):
		self.start = True
		self.total_points = 0
		self.deck = Deck()
		self.deck.shuffle()
		self.deck.transform_list_to_dequeue()
		# draw the first 5 cards for hand
		for i in range(0, 5):
			self.hand[i] = self.deck.q.popleft()
			self.hand[i].in_hand = True
			self.hand[i].in_deck = False

	# TODO: Implement card removal on mouse click
	# def throw_card(self):
	# - Goal: detect which card in self.hand the user clicks and remove it
	# - Steps:
	#     1. Determine card bounding boxes/positions and map mouse coordinates to a hand index.
	#     2. Validate the target card (exists and not already used).
	#     3. Update card state:
	#          card.in_hand = False
	#          card.in_deck = False
	#          card.used = True
	#     4. Remove the card from self.hand (or mark/replace according to game rules).
	#     7. Refresh UI / sprites and handle edge cases (empty deck, rapid clicks).

	#     * Right-clicking a visible hand card removes it and updates states without errors.
	#     * No exceptions on empty deck or fast repeated clicks.

	# Draws a card from the deck(as long as there are cards left) and places it in the hand
	def draw_card(self):
 	# TODO: Implement card  drawing when clicking the deck
	# TODO: Implement a way to stop the game when there are no cards in deck.q
		for i in range(0, 5):
			if self.hand[i] is None:
				if len(self.deck.q) != 0:
					self.hand[i] = self.deck.q.popleft()
					self.hand[i].in_hand = True
					self.hand[i].in_deck = False
				else:
					self.end = True
					break

	def debug_print_hand(self):
		for i in range(0, 5):
			print(f"self.hand[{i}], [{self.hand[i].number}, '{self.hand[i].color}'] ", end=' ')
			print()
			print(f"test_card: in_deck={self.hand[i].in_deck}, in_hand={self.hand[i].in_hand}, used={self.hand[i].used}")

class Card:
	# bool in_deck
	# bool in_combination
	# bool in_hand
	# bool used
	# int number
	# string color

	# At the start of each game
	def __init__(self, number, color):
		self.in_deck = True
		self.in_hand = False
		self.in_combination = False
		self.used = False
		self.number = number
		self.color = color
	
	def __init__(self, number=-1, color="No color"):
		self.in_deck = True
		self.in_hand = False
		self.in_combination = False
		self.used = False
		self.number = number
		self.color = color

	def set_fields_for_card_in_hand(self):
		self.in_deck = False
		self.in_hand = True

	def debug_print_card(self):
		test_card = self
		print(f"test_card: in_deck={test_card.in_deck}, in_hand={test_card.in_hand}, used={test_card.used}")
		print(f"test_card: {test_card.color}, {test_card.number}")
  

class Deck:
	# Card cards[24]
	# bool valid_shuffle
	# colors = ['red', 'blue', 'yellow']
	# numbers = [1, 2, 3, 4, 5, 6, 7, 8]

	def __init__(self):
		self.cards = []
		self.q = deque()
		# initialize the deck with cards
		for number in range(1, 9):
			for color in ['red', 'blue', 'yellow']:
				self.cards.append(Card(number, color))
		
	# Returns a well shuffled deck by calling the check_shuffle method
	def shuffle(self):
		random.shuffle(self.cards)
		while self.check_shuffle() == False:
			random.shuffle(self.cards)		
	
	# Returns True when the deck is well shuffled
	def check_shuffle(self):
		if self.has_big_pair() == True or self.has_three_same_color() == True:
			return False
		return True

	# Returns True if sequence contains consecutive numbers of the same color in cards > 5
	def has_big_pair(self):
		for curr_card, next_card in zip(self.cards, self.cards[1:]):
			if curr_card.number > 5 and curr_card.number == (next_card.number - 1) and curr_card.color == next_card.color:
				return True
		return False

	# Returns True if starting hand contains three cards of the same color
	def has_three_same_color(self):
		# dictionary: key = card.color, value = frequency of card.color
		color_counts = {}
		for Card in self.cards[:5]:
			color_counts[Card.color] = color_counts.get(Card.color, 0) + 1
			if color_counts[Card.color] >= 3:
				return True
		return False

	def print(self):
		for Card in self.cards:
			print(f'[{Card.number}, {Card.color}]', end=' ')
		print()

	def transform_list_to_dequeue(self):
		self.q = deque()
		for Card in self.cards:
			self.q.append(Card)

	def print_queue(self):
		for Card in self.q:
			print(f'[{Card.number}, {Card.color}]', end =' ')
		print()

# Returns True if the 3 cards have the same color
def same_color(combination_cards):
	c1 = combination_cards[0]
	c2 = combination_cards[1]
	c3 = combination_cards[2]
	if c1.color == c2.color == c3.color:
		return True
	return False

def calculate_points_per_move(combination_cards):
	c1 = combination_cards[0]
	c2 = combination_cards[1]
	c3 = combination_cards[2]
	
	temp_pts = 0
	# identical cards
	match (c1.number, c2.number, c3.number):
		case (1, 2, 3):
			temp_pts = 50 if same_color(combination_cards) else 10
		case (2, 3, 4):
			temp_pts = 60 if same_color(combination_cards) else 20
		case (3, 4, 5):
			temp_pts = 70 if same_color(combination_cards) else 30
		case (4, 5, 6):
			temp_pts = 80 if same_color(combination_cards) else 40
		case (5, 6, 7):
			temp_pts = 90 if same_color(combination_cards) else 50
		case (6, 7, 8):
			temp_pts = 100 if same_color(combination_cards) else 50
		case (x, y, z) if x == y == z:
			temp_pts = (x + 1) * 10

	return temp_pts

def main():
	game_state = GameState()
	game_state.start_game()
	game_state.debug_print_hand()
	
	pygame.init()
	screen = pygame.display.set_mode((screen_width, screen_height))
	pygame.display.set_caption("Card Game")
 
	clock = pygame.time.Clock()
 
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		
		screen.fill((25, 23, 22))
		pygame.display.flip()
		clock.tick(60)
		
	# print("Hello world!")
	# my_deck = Deck()
	# print("Instantiated deck")
	# my_deck.shuffle()
	# print("Shuffled deck")
	# my_deck.print()
	# my_deck.transform_list_to_dequeue()
	# print("Transformed to queue")
	# my_deck.print_queue()
	# print("\n")
	
	# test_card = my_deck.q[0]
	# test_card.debug_print_card()
 
	# for now, total points will be a global variable
	# combination_cards = [Card(4, 'red'), Card(5, 'red'), Card(6, 'red')]
	# for Card in my_deck.q:
	# 	combination_cards.append(Card)
	# total_pts = calculate_points_per_move(combination_cards)
	# print(total_pts)

if __name__ == "__main__":
	main()