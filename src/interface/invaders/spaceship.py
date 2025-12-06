import pygame
import math
from .utilities import *
from .constants import *

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, spritesheet, speed, acceleration, friction, velocity_limit, counter_strafe_multiplier, angle_increment):
        super().__init__()
        self.x = x
        self.y = y

        self.spritesheet = spritesheet

        self.speed = speed
        self.acceleration = acceleration
        self.friction = friction
        self.velocity_limit = velocity_limit
        self.counter_strafe_multiplier = counter_strafe_multiplier
        self.angle_increment = angle_increment

        self.angle = 0
        self.angle_sign = 0
        self.velocity = 0

    def update(self):
        keys = pygame.key.get_pressed()

        move_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        move_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]

        if move_left:
            if self.velocity > 0:
                self.velocity -= self.acceleration * self.counter_strafe_multiplier
            else:
                self.velocity -= self.acceleration
        elif move_right:
            if self.velocity < 0:
                self.velocity += self.acceleration * self.counter_strafe_multiplier
            else:
                self.velocity += self.acceleration
        else:
            # No input = normal friction
            if self.velocity > 0:
                self.velocity -= self.friction
                self.velocity = max(self.velocity, 0)
            elif self.velocity < 0:
                self.velocity += self.friction
                self.velocity = min(self.velocity, 0)

        self.velocity = max(-self.velocity_limit, min(self.velocity, self.velocity_limit))
        self.x += self.velocity
        if self.x < 50:
            self.x = 50
            self.velocity = 0
        elif self.x > 1920 - 150:
            self.x = 1920 - 150
            self.velocity = 0

        self.angle = (self.velocity // 5) * self.angle_increment * -1

        self.rect = spaceship_animation(self, self.spritesheet, pygame.time.get_ticks() // SPACESHIP_ANIMATION_SLOWDOWN % SPACESHIP_TOTAL_FRAMES)

    def draw(self, screen):
        rotated_spaceship = pygame.transform.rotozoom(self.rect, self.angle, 1)
        rotated_rect = rotated_spaceship.get_rect(center=(self.x + 50, self.y + 50))
        screen.blit(rotated_spaceship, rotated_rect.topleft)