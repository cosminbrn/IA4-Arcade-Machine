import os
import pygame

# --- SCALING ---
ORIGINAL_HEIGHT = 720
TARGET_HEIGHT = 1080
SCALE = TARGET_HEIGHT / ORIGINAL_HEIGHT # 1.5

GAME_W = 1440
GAME_H = 1080

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (123, 194, 212)
BARS_COLOR = (20, 20, 30)

# --- Game Settings ---
FLAKE_COUNT = 550
HAND_START_SPEED = 6 * SCALE
HAND_MAX_SPEED = 8.5 * SCALE
HAND_ACCEL = 0.02 * SCALE
HAND_RESPAWN_DELAY = 250
HAND_OFFSET_Y_RATIO = 0.6

# --- PATHS ---
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_PATH, "..", "..", "assets", "presents")