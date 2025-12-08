import pygame
import os
from observers import Observer
from commands import *

from settings import globals

# Constants for Layout
SCREEN_WIDTH = globals.VIRTUAL_WIDTH
SCREEN_HEIGHT = globals.VIRTUAL_HEIGHT

# Colors
COLOR_BG = (25, 25, 25)
COLOR_SLOT = (40, 40, 40)
COLOR_SLOT_BORDER = (100, 100, 100)
COLOR_TEXT = (255, 255, 255)
COLOR_GOLD = (255, 215, 0)
COLOR_RED = (200, 50, 50)
COLOR_BLUE = (50, 100, 200)
COLOR_YELLOW = (200, 200, 50)

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
            return None # Return None to trigger fallback drawing

    def load_font(self, size=24):
        key = f"font_{size}"
        if key in self.fonts:
            return self.fonts[key]
        font = pygame.font.SysFont("arial", size, bold=True)
        self.fonts[key] = font
        return font

class GameView(Observer):
    def __init__(self, model, screen):
        self.model = model
        self.real_screen = screen
        
        # Calculate scaling
        run_w, run_h = globals.WINWIDTH, globals.WINHEIGHT
        virt_w, virt_h = globals.VIRTUAL_WIDTH, globals.VIRTUAL_HEIGHT
        
        self.scale = min(run_w / virt_w, run_h / virt_h)
        self.offset_x = (run_w - virt_w * self.scale) // 2
        self.offset_y = (run_h - virt_h * self.scale) // 2
        
        self.screen = pygame.Surface((virt_w, virt_h)) # Virtual Surface for drawing
        
        self.rm = ResourceManager()
        self.model.attach(self)
        
        # UI Metrics
        self.card_width = 100
        self.card_height = 140
        self.hand_y = 100    # Top of screen
        self.combo_y = 400   # Middle
        self.deck_y = 700    # Bottom Left
        self.deck_x = 50
        
        # Pre-calculate Rects for click detection
        self.hand_rects = []
        start_x = (SCREEN_WIDTH - (5 * 110)) // 2
        for i in range(5):
            self.hand_rects.append(pygame.Rect(start_x + i * 110, self.hand_y, self.card_width, self.card_height))
            
        self.combo_rects = []
        start_x_combo = (SCREEN_WIDTH - (3 * 110)) // 2
        for i in range(3):
            self.combo_rects.append(pygame.Rect(start_x_combo + i * 110, self.combo_y, self.card_width, self.card_height))
            
        self.deck_rect = pygame.Rect(self.deck_x, self.deck_y, self.card_width, self.card_height)

    def update(self, subject):
        # React to model changes
        self.draw()

    def draw(self):
        # Background - Simplified as requested
        # Using a nice dark slate colors scheme for premium feel
        self.screen.fill((30, 35, 45)) 

        # Draw Slots (Visual placeholders)
        for rect in self.hand_rects:
            self.draw_slot(rect, "Hand")
            
        for rect in self.combo_rects:
             self.draw_slot(rect, "Combo")
             
        # Draw Deck with Stack Effect
        if not self.model.deck.is_empty():
            count = len(self.model.deck.cards)
            # Visualize up to 5 cards for the stack effect
            visual_count = min(count, 5)
            
            # Draw from bottom to top
            for i in range(visual_count):
                # Calculate offset: bottom cards are shifted slightly
                # We want the top card (last drawn) to be at self.deck_rect
                # Cards below slightly down/right or up/left. 
                # Let's shift "lower" cards down and right slightly so top is top-left-most? 
                # Or usually top is "highest". Let's shift lower cards by (offset, offset)
                
                # Reverse index for offset: 0 is top, 4 is bottom
                # We are drawing loop 0..4. 
                # Let's say we draw bottom first.
                
                layer_idx = visual_count - 1 - i # 4, 3, 2, 1, 0
                offset = layer_idx * 2
                
                draw_rect = self.deck_rect.move(offset, offset)
                self.draw_card_back(draw_rect)

            # Draw Count
            font = self.rm.load_font(20)
            text = font.render(f"x {count}", True, COLOR_TEXT)
            # Position text relative to the main deck rect
            self.screen.blit(text, (self.deck_rect.right + 15, self.deck_rect.centery))
        
        # Draw Cards in Hand
        for i, card in enumerate(self.model.hand):
            if card:
                self.draw_card(card, self.hand_rects[i])

        # Draw Cards in Combo
        for i, card in enumerate(self.model.combination):
            if card:
                self.draw_card(card, self.combo_rects[i])

        # Draw Score
        font_score = self.rm.load_font(40)
        score_text = font_score.render(f"Score: {self.model.score}", True, COLOR_GOLD)
        self.screen.blit(score_text, (SCREEN_WIDTH - 250, 750))
        
        # Draw Message
        if self.model.message:
            font_msg = self.rm.load_font(30)
            msg_text = font_msg.render(self.model.message, True, COLOR_TEXT)
            rect = msg_text.get_rect(center=(SCREEN_WIDTH//2, 600))
            self.screen.blit(msg_text, rect)

        # Final Blit to Real Screen
        scaled_w = int(globals.VIRTUAL_WIDTH * self.scale)
        scaled_h = int(globals.VIRTUAL_HEIGHT * self.scale)
        scaled_surface = pygame.transform.scale(self.screen, (scaled_w, scaled_h))
        
        self.real_screen.fill((0, 0, 0)) # Black bars
        self.real_screen.blit(scaled_surface, (self.offset_x, self.offset_y))
        pygame.display.flip()

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
        # Expected naming: "cards/red_1.png", "cards/blue_5.png"
        image_key = f"cards/{card.color}_{card.number}.png"
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
        pygame.draw.rect(self.screen, (40, 120, 60), rect, border_radius=4) # Darker Green
        pygame.draw.rect(self.screen, (220, 220, 220), rect, 2, border_radius=4) # White/Grey Border
        
        # Simple Pattern (Diamond in center)
        cx, cy = rect.centerx, rect.centery
        pygame.draw.circle(self.screen, (60, 140, 80), (cx, cy), 15)


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
                
        return None
