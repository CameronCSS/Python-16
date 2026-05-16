"""
Boss class — a massive enemy that appears at 50k milestones
"""
import os
import random
import pygame
from settings import *

class Boss:
    def __init__(self, is_mega=False):
        img_name = MEGA_BOSS_IMG if is_mega else BOSS_IMG
        self.img = pygame.image.load(os.path.join(IMAGES_PATH, img_name))
        self.laser_img = pygame.image.load(os.path.join(IMAGES_PATH, 'laser2.png'))
        self.is_mega = is_mega
        
        # Start at the top center
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = (SCREEN_WIDTH // 2) - (self.width // 2)
        self.y = -self.height # Start off-screen
        
        self.x_change = 2 if is_mega else 3 # Mega is slightly slower/heavier
        self.y_change = 0.3 if is_mega else 0.5 
        self.max_hp = 60 if is_mega else 20
        self.hp = self.max_hp
        
        # Dual lasers
        self.fire_mult = 0.6 if is_mega else 0.4 # Mega shoots slower now

        # Boss explosion system (3x3 spritesheet)
        ex_name = 'boss_explosions2.png' if is_mega else 'boss_explosions.png'
        self.explosion_sheet = pygame.image.load(os.path.join(IMAGES_PATH, ex_name)).convert_alpha()
        self.explosion_frames = []
        frame_w = self.explosion_sheet.get_width() // 3
        frame_h = self.explosion_sheet.get_height() // 3
        
        for row in range(3):
            for col in range(3):
                frame = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
                frame.blit(self.explosion_sheet, (0, 0), (col * frame_w, row * frame_h, frame_w, frame_h))
                # Scale to 256x256 for a massive boss explosion
                self.explosion_frames.append(pygame.transform.scale(frame, (256, 256)))
                
        self.is_exploding = False
        self.explosion_timer = 0
        self.explosion_duration = 45 # 9 frames * 5 ticks per frame

    def update(self):
        """Boss movement pattern or explosion update"""
        if self.is_exploding:
            self.explosion_timer += 1
            return self.explosion_timer >= self.explosion_duration

        self.y += self.y_change
        self.x += self.x_change
        
        # Stop descending at y=100
        if self.y > 100:
            self.y = 100
            
        # Bounce off walls
        if self.x <= 10 or self.x >= SCREEN_WIDTH - self.width - 10:
            self.x_change *= -1
        return False

    def draw(self, screen):
        """Draw the boss or its explosion"""
        if self.is_exploding:
            frame_idx = min(len(self.explosion_frames)-1, self.explosion_timer // 5)
            # Center the massive explosion
            ex_x = self.x + self.width // 2 - 128
            ex_y = self.y + self.height // 2 - 128
            screen.blit(self.explosion_frames[frame_idx], (ex_x, ex_y))
            return

        screen.blit(self.img, (self.x, self.y))
        
        # Simple health bar
        if self.hp > 0:
            bar_width = self.width
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 20, bar_width, 10))
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 20, bar_width * (self.hp / self.max_hp), 10))

    def hit(self):
        """Take damage"""
        if self.is_exploding:
            return False
        self.hp -= 1
        if self.hp <= 0:
            self.is_exploding = True
            return True
        return False
