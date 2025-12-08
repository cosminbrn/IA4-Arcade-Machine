import pygame
import os

# Module that implements assets and font loading

class ResourceManager:
	def __init__(self, assets_dir="assets"):
		self.assets_dir = assets_dir
		self.images = {}
		self.fonts = {}

	def load_image(self, path, size=None):
		if path in self.images:
			return self.images[path]

		full_path = os.path.join(self.assets_dir, path)
		try:
			img = pygame.image.load(full_path).convert_alpha()
			if size:
				img = pygame.transform.scale(img, size)
			self.images[path] = img
			return img
		except:
			return None

	def load_font(self, size=24):
		key = f"font_{size}"
		if key in self.fonts:
			return self.fonts[key]
		try:
			font = pygame.font.SysFont("Tahoma", size, bold=False)
		except:
			font = pygame.font.SysFont("arial", size, bold=True)
			
		self.fonts[key] = font
		return font
