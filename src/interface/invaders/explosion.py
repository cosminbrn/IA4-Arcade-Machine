import pygame
from .constants import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet):
        super().__init__()
        self.frames = []
        for i in range(EXPLOSION_TOTAL_FRAMES):
            frame_x = (i % EXPLOSION_SPRITESHEET_COLUMNS) * EXPLOSION_FRAME_WIDTH
            frame_y = (i // EXPLOSION_SPRITESHEET_COLUMNS) * EXPLOSION_FRAME_HEIGHT
            frame_surface = pygame.Surface((EXPLOSION_FRAME_WIDTH, EXPLOSION_FRAME_HEIGHT), pygame.SRCALPHA)
            frame_surface.blit(spritesheet, (0, 0), (frame_x, frame_y, EXPLOSION_FRAME_WIDTH, EXPLOSION_FRAME_HEIGHT))
            scaled_frame = pygame.transform.scale(frame_surface, (EXPLOSION_WIDTH, EXPLOSION_HEIGHT))
            self.frames.append(scaled_frame)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = EXPLOSION_ANIMATION_SLOWDOWN // EXPLOSION_TOTAL_FRAMES  # ms per frame

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]
            else:
                self.kill()  # remove sprite when animation is done